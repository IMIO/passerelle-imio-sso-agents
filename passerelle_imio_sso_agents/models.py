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
import decimal

from django.db import models
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint



class ImioSsoAgents(BaseResource):

    category = _('Datasources manager')
    csv_file = models.FileField(_('Agents csv file'), upload_to='agents_csv',
        help_text=_('Supported file formats: csv'))
    
    ignore_types =  models.CharField(_('Types to ignore'), default='', max_length=128, blank=True)
    
    class Meta:
        verbose_name = _("imio.memory CSV to JSON that be comsumme by WCA.")

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name
    @classmethod
    def get_icon_class(cls):
        return ''

    def save(self, *args, **kwargs):
        result = super(ImioSsoAgents, self).save(*args, **kwargs)
        return result

    def get_content_without_bom(self):
        self.csv_file.seek(0)
        content = self.csv_file.read()
        return content.decode('utf-8-sig', 'ignore').encode('utf-8')

    def get_rows(self):
        file_type = self.csv_file.name.split('.')[-1]
        if file_type == 'csv':
            content = self.get_content_without_bom()
            reader = csv.reader(content.splitlines(), delimiter=',')
            rows = list(reader)
        return rows



    def add_app(mun_id, app_id):
        url = "{0}/{1}/{2}".format(memroy_base_url, app_name, mun_id)
        req = requests.get(url)
        if req.status_code == 404:
            add_municipality(mun_id)
        req = requests.get(url)
        if app_id not in req.json():
            params = {"container_id": app_id}
            req = requests.post(url, json=params)

    @endpoint(perm='can_access', methods=['get'])
    def export_to_memory(self, users):
        add_app(mun_id, app_id)
        line_count = 0
        for user in users:
            add_user(user)
            line_count += 1

    @endpoint(perm='can_access', methods=['get'])
    def json(self, request, **kwargs):
        keys = []
        agents = []
        rows = self.get_rows()
        for r in rows:
            num_col = 0
            if rows.index(r) == 0:
                for col in r:
                    keys.append(col)
            else:
                allowed_services = []
                agent = {}
                current_municipality_id = ''
                for col in r:
                    agent.update( {keys[num_col]:col} )
                    if keys[num_col] == 'municipality_id':
                        current_municipality_id = col
                    if keys[num_col].startswith('old') and keys[num_col].endswith('userid') and r[num_col] != '':
                        service = '{0}-{1}'.format(current_municipality_id, keys[num_col].split('_')[1].replace('.','').lower())
                        allowed_services.append(service)
                    num_col = num_col + 1
                agent.update( {"allowed_services":allowed_services} )
                agents.append(agent)
        return {'data':agents}
