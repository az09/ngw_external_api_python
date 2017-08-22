# -*- coding: utf-8 -*-
"""
/***************************************************************************
    NextGIS WEB API
                              -------------------
        begin                : 2014-11-19
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import requests

from os import path
from ngw_resource import NGWResource

from ..utils import ICONS_DIR


class NGWWmsLayer(NGWResource):

    type_id = 'wmsclient_layer'
    icon_path = path.join(ICONS_DIR, 'wms_layer.svg') # TODO change icon
    type_title = 'NGW WMS Layer'

    def __init__(self, resource_factory, resource_json):
        NGWResource.__init__(self, resource_factory, resource_json)

    @classmethod
    def create_in_group(cls, name, ngw_group_resource, ngw_wms_connection_id, wms_layers):
        connection = ngw_group_resource._res_factory.connection
        url = ngw_group_resource.get_api_collection_url()

        params = dict(
            resource=dict(
                cls=cls.type_id,
                display_name=name,
                parent=dict(
                    id=ngw_group_resource.common.id
                )
            )
        )

        params[cls.type_id] = dict(
            connection=dict(
                id=ngw_wms_connection_id
            ),
            wmslayers=wms_layers,
            imgformat="image/png",
            srs=dict(
                id=3857
            ),
        )

        try:
            result = connection.post(url, params=params)

            ngw_resource = cls(
                ngw_group_resource._res_factory,
                NGWResource.receive_resource_obj(
                    connection,
                    result['id']
                )
            )

            return ngw_resource
        except requests.exceptions.RequestException, e:
            raise NGWError('Cannot create wfs layer. Server response:\n%s' % e.message)