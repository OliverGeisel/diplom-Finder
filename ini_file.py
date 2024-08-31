import typing_extensions


class IniRegion:
    def __init__(self, name):
        self.name = name
        self.data = dict()

    def __getitem__(self, key) -> str:
        return self.data[key]

    def __setitem__(self, key, value) -> None:
        self.data[key] = value

    def __delitem__(self, key) -> None:
        del self.data[key]

    def __iter__(self) -> typing_extensions.Iterable[str]:
        return self.data.keys()

    def values(self) -> typing_extensions.Iterable[str]:
        return self.data.values()

    def items(self) -> typing_extensions.Iterable[tuple[str, str]]:
        return self.data.items()

    def __len__(self) -> int:
        return len(self.data)


class IniFile:
    def __init__(self, filename):
        self.filename = filename
        self.regions = {}

    def read(self):
        with open(self.filename) as f:
            region = None
            for line in f:
                line = line.strip()
                if line.startswith('['):
                    region = IniRegion(line[1:-1])
                    self.regions[region.name] = region
                else:
                    key, value = line.split('=', 1)
                    region[key.strip()] = value.strip()

    def write(self):
        with open(self.filename, 'w') as f:
            for region in self.regions.values():
                f.write(f'[{region.name}]\n')
                for key, value in region.data.items():
                    f.write(f'{key} = {value}\n')

    def __getitem__(self, key) -> IniRegion:
        return self.regions[key]

    def __setitem__(self, key: str, value: IniRegion) -> None:
        self.regions[key] = value

    def __delitem__(self, key) -> None:
        del self.regions[key]

    def __iter__(self) -> typing_extensions.Iterable[IniRegion]:
        return iter(self.regions.keys())

    def __len__(self) -> int:
        return len(self.regions)

    def total_keys(self) -> int:
        return sum(len(region) for region in self.regions.values())
