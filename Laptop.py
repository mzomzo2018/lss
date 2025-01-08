class Laptop:
    def __init__(self):
        self._manufacturer = ""
        self._model_family = ""
        self._model = ""
        self._cpu = ""
        self._integrated_gpu = ""
        self._dedicated_gpu = ""
        self._ram = ""
        self._storage = ""
        self._storage_type = ""
        self._drivers = []

    # Manufacturer property
    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter 
    def manufacturer(self, value):
        self._manufacturer = value

    # Model family property
    @property
    def model_family(self):
        return self._model_family

    @model_family.setter
    def model_family(self, value):
        self._model_family = value

    # Model property
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    # CPU property
    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, value):
        self._cpu = value

    # Integrated GPU property
    @property
    def integrated_gpu(self):
        return self._integrated_gpu

    @integrated_gpu.setter
    def integrated_gpu(self, value):
        self._integrated_gpu = value

    # Dedicated GPU property
    @property
    def dedicated_gpu(self):
        return self._dedicated_gpu

    @dedicated_gpu.setter
    def dedicated_gpu(self, value):
        self._dedicated_gpu = value

    # RAM property
    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, value):
        self._ram = value

    # Storage property
    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = value

    # Storage type property
    @property
    def storage_type(self):
        return self._storage_type

    @storage_type.setter
    def storage_type(self, value):
        self._storage_type = value

    # Drivers property
    @property
    def drivers(self):
        return self._drivers

    @drivers.setter
    def drivers(self, value):
        self._drivers = value
