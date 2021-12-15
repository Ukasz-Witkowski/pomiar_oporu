class Wykres_dynamiczny_1(Figura_wykresu):
    def load_default_path(self):
        f = open('config.json')
        data = json.load(f)
        default_path = data['default_path']
        f.close()
        return default_path

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)
        self.nasz_miernik = miernik20.Aparature()
        self.default_path = self.load_default_path()

    def compute_initial_figure(self):
        self.y_var=[random.randint(0, 10) for i in range(10)]
        self.x_var=[i for i in range (10)]
        self.axes.plot(self.x_var,self.y_var, 'r')

    def update_figure(self):

        data = float(self.nasz_miernik.mierz())
        #print(data)
        # print(self.default_path)
        with open(self.default_path,"a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), data])
        self.y_var = np.append(self.y_var, data )
        self.y_var = self.y_var[1 : ]

        self.axes.cla()
        self.axes.plot(self.x_var, self.y_var, 'b')
        self.draw()