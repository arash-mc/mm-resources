def deconstruct_single(single, nx, ny):
    block = {}
    for j in range(ny):
        block[j] = {}
    shape = single.shape
    yd = int(shape[0] / ny)
    xd = int(shape[1] / nx)
    for indy in range(ny):
        for indx in range(nx):
            block[indy][indx] = single[indy * yd:(indy + 1) * yd - 1, indx * xd:(indx + 1) * xd - 1, :]
    return block


def deconstruct_all(output, key='m'):
    nx = len(output['parameters']['inner_values'])
    ny = len(output['parameters']['outer_values'])
    deconstructed = {}
    for index, item in enumerate(output['data'][key]):
        deconstructed[index] = deconstruct_single(item, nx, ny)
    return deconstructed
def make_list_of_zeros(nx,ny):
    l = list()
    for i in range(ny):
        l.append(list())
        for j in range(nx):
            l[i].append(0)
    return l
def make_list_of_nones(nx,ny):
    l = list()
    for i in range(ny):
        l.append(list())
        for j in range(nx):
            l[i].append(None)
    return l


class AutoCheck():
    def __init__(self, viewobj, criteria, key='m'):
        self.viewobj = viewobj
        self.criteria = criteria
        self.key = key

    def diagrams(self):
        nx = self.viewobj.nx
        ny = self.viewobj.ny
        deconstructed = deconstruct_all(self.viewobj.output, key=self.key)
        self.diagram, self.diagramn = self.extract_phase_diagram(self.criteria, deconstructed, nx, ny)
        return self.diagram, self.diagramn

    def extract_phase_diagram(self, f, deconstructed, nx, ny):
        phase_diagram = make_list_of_zeros(nx, ny)
        phase_diagramn = make_list_of_nones(nx, ny)
        for frame in sorted(deconstructed.keys(), reverse=True):  # reverse because we want to have the first occurance
            for indy in deconstructed[frame].keys():
                for indx in deconstructed[frame][indy].keys():
                    image = deconstructed[frame][indy][indx]
                    if f(image):
                        phase_diagramn[indy][indx] = frame
        for indy in range(ny):
            for indx in range(nx):
                if phase_diagramn[indy][indx] is not None:
                    phase_diagram[indy][indx] = 1

        return phase_diagram, phase_diagramn

