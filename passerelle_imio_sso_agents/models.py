# passerelle-imio-sso-agents - passerelle connector
# Copyright (C) 2016  Entr'ouvert / Imio
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import six

from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint


class ImioSsoAgents(BaseResource):

    category = _("Datasources manager")
    csv_file = models.FileField(
        _("Agents csv file"),
        upload_to="agents_csv",
        help_text=_("Supported file formats: csv"),
    )

    ignore_types = models.CharField(
        _("Types to ignore"), default="", max_length=128, blank=True
    )
    locality_name = models.CharField(
        _("Locality name"), default="", max_length=128, blank=True
    )
    locality_slug = models.CharField(
        _("Locality slug (enterprise number)"), default="", max_length=128, blank=True
    )

    # services_client_id
    # services_client_secret
    # services_frontchannel_logout_uri
    all_services = []

    class Meta:
        verbose_name = _("imio.memory CSV to JSON that be comsumme by WCA.")

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_icon_class(cls):
        return ""

    def save(self, *args, **kwargs):
        kwargs.pop("cache", False)
        result = super(ImioSsoAgents, self).save(*args, **kwargs)
        return result

    def _detect_dialect_options(self):
        content = self.get_content_without_bom()
        dialect = csv.Sniffer().sniff(content)
        self.dialect_options = {
            k: v for k, v in vars(dialect).items() if not k.startswith("_")
        }

    @property
    def dialect_options(self):
        """turn dict items into string
        """
        file_type = self.meal_file.name.split(".")[-1]
        if file_type in ("ods", "xls", "xlsx"):
            return None
        # Set dialect_options if None
        # if self._dialect_options is None:
        self._detect_dialect_options()
        self.save(cache=False)

        options = {}
        for k, v in self._dialect_options.items():
            if isinstance(v, six.text_type):
                v = force_str(v.encode("ascii"))
            options[force_str(k.encode("ascii"))] = v

        return options

    @dialect_options.setter
    def dialect_options(self, value):
        self._dialect_options = value

    def get_content_without_bom(self):
        self.csv_file.seek(0)
        content = self.csv_file.read()
        return force_str(content.decode("utf-8-sig", "ignore").encode("utf-8"))

    def get_rows(self):
        file_type = self.csv_file.name.split(".")[-1]
        if file_type == "csv":
            content = self.get_content_without_bom()
            reader = csv.reader(content.splitlines(), delimiter=",")
            rows = list(reader)
        return rows

    # def add_app(mun_id, app_id):
    #     url = "{0}/{1}/{2}".format(memroy_base_url, app_name, mun_id)
    #     req = requests.get(url)
    #     if req.status_code == 404:
    #         add_municipality(mun_id)
    #     req = requests.get(url)
    #     if app_id not in req.json():
    #         params = {"container_id": app_id}
    #         req = requests.post(url, json=params)
    #
    # @endpoint(perm="can_access", methods=["get"])
    # def export_to_memory(self, users):
    #     self.add_app(mun_id, app_id)
    #     line_count = 0
    #     for user in users:
    #         add_user(user)
    #         line_count += 1

    def locality(self):
        return {"name": self.locality_name, "slug": self.locality_slug}

    def get_different_services(self):
        return {v["slug"]: v for v in self.all_services}.values()

    def services(self, service_slug):
        service = {
            "client_id": "",  # puppet
            "client_secret": "",  # puppet
            "frontchannel_logout_uri": "https://.../logout",  # puppet
            "name": service_slug.replace("-", " "),  # puppet
            "open_to_all": False,
            "post_logout_redirect_uris": [""],
            "redirect_uris": [""],
            "slug": service_slug,
        }
        self.all_services.append(service)

    @endpoint(perm="can_access", methods=["get"])
    def json(self, request, **kwargs):
        rows = self.get_rows()
        keys = []
        agents = []
        for r in rows:
            num_col = 0
            # csv header (Agent keys)
            if rows.index(r) == 0:
                for col in r:
                    keys.append(col)
            # build agent
            else:
                allowed_services = []
                agent = {}
                current_municipality_id = ""
                for col in r:
                    agent.update({keys[num_col]: col})
                    if keys[num_col] == "municipality_id":
                        current_municipality_id = col
                    if (
                        keys[num_col].startswith("old")
                        and keys[num_col].endswith("userid")
                        and r[num_col] != ""
                    ):
                        service_slug = "{0}-{1}".format(
                            current_municipality_id,
                            keys[num_col].split("_")[1].replace(".", "").lower(),
                        )
                        self.services(service_slug)
                        allowed_services.append(service_slug)
                    if keys[num_col] == "content_id":
                        agent["username"] = col
                    if keys[num_col] == "user_id" and keys[num_col]:
                        agent["username"] = col
                    num_col = num_col + 1
                agent.update({"allowed_services": allowed_services})
                agents.append(agent)
        json = {}
        json["locality"] = self.locality()
        json["users"] = agents
        json["services"] = self.get_different_services()
        return json
