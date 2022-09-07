import xml.etree.ElementTree as ET
import re


def main():
    # KML parse
    tree = ET.parse('maps.kml')
    root = tree.getroot()

    # Identify default namespace
    namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
    ns = {'def': namespace}

    # Define coordinates RegEx
    coord_ex = '(-?\d+\.\d+),'
    heig_ex = '(\d+)'
    regex = coord_ex + coord_ex + heig_ex

    # Create output files (overwrite if already exist)
    with open('output_pins.py', 'w') as out_pin:
              # open('output_paths.txt', 'w') as out_pat, \
              # open('output_polygons.txt', 'w') as out_pol:

        # Add headers -- original headers were replaced by beginning of google map link.. originally were 
        out_pin.write('https://www.google.com/maps/dir/')
        # out_pat.write('https://www.google.com/maps/dir/')
        # out_pol.write('https://www.google.com/maps/dir/')

        # Find coordinates
        for i in root.findall('.//def:Placemark', ns):
            # name = i.find('def:name', ns).text
            coord = i.find('.//def:coordinates', ns)
            # Check for placeless placemark
            if not coord is None:
                coord = coord.text.strip()
                coord = re.findall(regex, coord)
                # Save data
                pin = 0
                for (long, lat, heig) in coord:
                    pin += 1
                    if i.find('.//def:Point', ns):
                        out_pin.write(f'{lat},{long}/')
                    elif i.find('.//def:LineString', ns):
                        out_pat.write(f'{lat},{long}/')
                    elif i.find('.//def:Polygon', ns):
                        out_pol.write(f'{lat},{long}/')


if __name__ == '__main__':
    main()
