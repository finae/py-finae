import re
import pprint

import finae

# Example of LLM results
input = """
To determine the top 50 mountains in the world, we will use a combination of factors such as height, difficulty, and cultural significance. Here is our list of the top 50 mountains in the world:

1. Mount Everest (Nepal/China) - 8,848 meters (29,029 ft)
2. K2 (Pakistan) - 8,611 meters (28,251 ft)
3. Kangchenjunga (Nepal/India) - 8,586 meters (28,169 ft)
4. Lhotse (Nepal/China) - 8,516 meters (27,940 ft)
5. Makalu (Nepal/China) - 8,463 meters (27,766 ft)
6. Cho Oyu (Nepal/China) - 8,201 meters (26,906 ft)
7. Dhaulagiri (Nepal) - 8,167 meters (26,811 ft)
8. Manaslu (Nepal) - 8,163 meters (26,808 ft)
9. Nanga Parbat (Pakistan) - 8,126 meters (26,660 ft)
10. Annapurna (Nepal) - 8,091 meters (26,545 ft)
11. Gasherbrum I (Pakistan) - 8,080 meters (26,513 ft)
12. Shishapangma (China) - 8,027 meters (26,341 ft)
13. Broad Peak (Pakistan) - 8,051 meters (26,414 ft)
14. Gyachung Kang (Nepal/China) - 7,952 meters (26,089 ft)
15. Pumori (Nepal/China) - 7,817 meters (25,647 ft)
16. Ama Dablam (Nepal) - 6,856 meters (22,494 ft)
17. Mount Kilimanjaro (Tanzania) - 5,895 meters (19,341 ft)
18. Mount Elbrus (Russia) - 5,642 meters (18,510 ft)
19. Denali (formerly known as Mount McKinley, USA) - 6,190 meters (20,310 ft)
20. Mount Vinson (Antarctica) - 4,892 meters (16,050 ft)
21. Aconcagua (Argentina) - 6,962 meters (22,841 ft)
22. Mount Kenya (Kenya) - 5,199 meters (17,057 ft)
23. Mount Cameroon (Cameroon) - 4,040 meters (13,255 ft)
24. Mount Rwenzori (Uganda) - 5,109 meters (16,763 ft)
25. Mount Nyiragongo (DR Congo) - 3,470 meters (11,385 ft)
26. Mount Meru (Tanzania) - 4,565 meters (14,980 ft)
27. Mount Ararat (Turkey) - 5,137 meters (16,854 ft)
28. Mount Damavand (Iran) - 5,610 meters (18,376 ft)
29. Mount Kazbek (Georgia) - 5,047 meters (16,558 ft)
30. Mount Ararat (Armenia) - 3,997 meters (13,110 ft)
31. Mount Sabi (Indonesia) - 3,680 meters (12,077 ft)
32. Mount Rinjani (Indonesia) - 3,726 meters (12,224 ft)
33. Mount Bromo (Indonesia) - 2,329 meters (7,642 ft)
34. Mount Kinabalu (Malaysia) - 4,095 meters (13,435 ft)
35. Mount Apo (Philippines) - 2,954 meters (9,692 ft)
36. Mount Pico (Portugal) - 2,351 meters (7,714 ft)
37. Mount Teide (Spain) - 3,718 meters (12,198 ft)
38. Mount Vesuvius (Italy) - 1,281 meters (4,203 ft)
39. Mount Etna (Italy) - 3,329 meters (10,922 ft)
40. Mount Popocatepetl (Mexico) - 5,426 meters (17,802 ft)
41. Mount Fuji (Japan) - 3,776 meters (12,388 ft)
42. Mount Aso (Japan) - 1,592 meters (5,223 ft)
43. Mount Yasur (Vanuatu) - 361 meters (1,184 ft)
44. Mount Guntur (Indonesia) - 3,646 meters (11,994 ft)
45. Mount Batur (Indonesia) - 7,360 meters (24,144 ft)
46. Mount Slamet (Indonesia) - 3,428 meters (11,246 ft)
47. Mount W Guyon (Vanuatu) - 2,460 meters (8,071 ft)
48. Mount Hood (Oregon, USA) - 3,429 meters (11,249 ft)
49. Mount Rainier (Washington, USA) - 4,392 meters (14,411 ft)
50. Mount Whitney (California, USA) - 4,421 meters (14,505 ft)

Note: Some of the heights listed may vary depending on the source and method of measurement.
"""


@finae.Concept
class Mountain:

    @finae.Attribute(weight=0.01, required=False)
    def index(self):
        parts = self.text().split('.')
        i = int(parts[0])
        assert 1 <= i <= 100
        return i

    @finae.Attribute
    def long_name(self):
        parts = self.text().split('.')[1].split('-')
        return parts[0].strip()

    @finae.Attribute
    def name(self):
        l = self.long_name()
        return l[:l.find('(')].strip()

    def name_make_sense(self):
        name = self.name()
        prompt = f'Is {name} a mountain? yes or no'
        print('------')
        print(prompt)
        r = finae.ask_llm(prompt)
        print('------')
        print(r)

    @finae.Attribute
    def location(self):
        l = self.long_name()
        c = l[l.find('(')+1:l.find(')')].strip()
        assert c
        return c

    @finae.Attribute
    def altitude_in_meters(self):
        m = re.search(r'[\d\s,]+m', self.text())
        if m:
            return int(m.group(0).replace('m', '').replace(',', '').strip())
        m = re.search(r'[\d,]+meters', self.text)
        if m:
            return int(m.group(0).replace('meters', '').replace(',', '').strip())
        raise ValueError(f'can not find meters in : {self.text()}')

    @finae.Attribute(required=False)
    def altitude_in_ft(self):
        m = re.search(r'[\d\s,]+ft', self.text())
        if m:
            return int(m.group(0).replace('ft', '').replace(',', '').strip())
        m = re.search(r'[\d,]+feet', self.text())
        if m:
            return int(m.group(0).replace('feet', '').replace(',', '').strip())
        raise ValueError(f'can not find feet in : {self.text()}')

    def __str__(self):
        return f'{self.index()}, {self.name()}, {self.location()}, {self.altitude_in_meters()} m, {self.altitude_in_ft()} ft'


def parse(input):
    mountains = []
    lines = input.split('\n')
    for line in lines:
        m = Mountain(line)
        if m.score() > 0.9:
            print(m, m.score())
            mountains.append(m)

    Mountain.__finae_debug__()
    # pprint.pprint(mountains[0].__finae_data__)

    # for m in mountains:
    #     m.name_make_sense()


if __name__ == '__main__':
    parse(input)
