# telegraph-figures

Illustrations for articles published on [Telegraph](https://telegra.ph). Telegraph's API has no file upload, so pages reference images by URL.

| Folder | Article |
| --- | --- |
| `phd-options/` | [Аспирантура по математике после магистратуры: какие есть варианты](https://telegra.ph/Aspirantura-po-matematike-posle-magistratury-kakie-est-varianty-10-04) |

## phd-options

`spouse_map.py` draws the spouse status map. It needs the Natural Earth 1:50m admin-0 countries shapefile (public domain, <https://www.naturalearthdata.com>) unpacked next to the script:

```sh
curl -LO https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip
unzip ne_50m_admin_0_countries.zip
uv run --no-project --with geopandas --with matplotlib --with pyogrio python spouse_map.py
```
