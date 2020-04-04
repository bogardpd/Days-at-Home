""" Creates an SVG chart from trip and home stay data. """

import xml.etree.ElementTree as xml


class SVGChart:
    
    PARAMS = {
        'day_box': {
            'size': 8, # px
            'stroke': '#ffffff',
            'stroke_width': 1,
            'home': {
                'fill': '#55c4b4',
            },
            'trip': {
                'fill': '#758fd1',
            }
        },
        'page': {
            'margin': 40, # px
        },        
    }

    def __init__(self, stays_collection):
        self.stays = stays_collection

    def export(self, output_path):
        """
        Generates an SVG chart based on the trip/home row values.
        """
                
        max_trip = max(x['trip']['duration'] for x in self.stays)
        max_home = max(x['home']['duration'] for x in self.stays)
        trip_home_divider_x_pos = (
            self.PARAMS['page']['margin']
            + (max_trip * self.PARAMS['day_box']['size']))

        doc_width = (
            (2 * self.PARAMS['page']['margin'])
            + ((max_trip + max_home) * self.PARAMS['day_box']['size']))
        doc_height = (
            (2 * self.PARAMS['page']['margin'])
            + (len(self.stays) * self.PARAMS['day_box']['size']))
        
        root = xml.Element(
            "svg", width=str(doc_width), height=str(doc_height))
        
        for row_index, row in enumerate(self.stays):
            y_pos = (
                self.PARAMS['page']['margin']
                + (row_index * self.PARAMS['day_box']['size']))
            
            for trip_index in range(row['trip']['duration']):
                x_pos = (
                    trip_home_divider_x_pos
                    - (
                        (1 + trip_index)
                        * self.PARAMS['day_box']['size']))
                
                xml.SubElement(
                    root, "rect", x=str(x_pos), y=str(y_pos),
                    width=str(self.PARAMS['day_box']['size']),
                    height=str(self.PARAMS['day_box']['size']),
                    fill=self.PARAMS['day_box']['trip']['fill'],
                    stroke=self.PARAMS['day_box']['stroke'],
                    stroke_width=str(
                        self.PARAMS['day_box']['stroke_width']))
            
            for home_index in range(row['home']['duration']):
                x_pos = (
                    trip_home_divider_x_pos
                    + (home_index * self.PARAMS['day_box']['size']))
                
                xml.SubElement(
                    root, "rect", x=str(x_pos), y=str(y_pos),
                    width=str(self.PARAMS['day_box']['size']),
                    height=str(self.PARAMS['day_box']['size']),
                    fill=self.PARAMS['day_box']['home']['fill'],
                    stroke=self.PARAMS['day_box']['stroke'],
                    stroke_width=str(
                        self.PARAMS['day_box']['stroke_width']))

        tree = xml.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"Wrote SVG to {output_path}")