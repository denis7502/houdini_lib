import hou


class ObjContext():
    def __init__(self):
        (self.sel_nd, self.editor, self.cursor,
            self.net, self.child, self.sel_c_nd) = self.update()

    def update(self):
        sel_nd = [i for i in hou.selectedItems()]
        editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        cursor = editor.cursorPosition()
        net = editor.pwd()
        child = net.children()
        sel_c_nd = len(sel_nd)

        return sel_nd, editor, cursor, net, child, sel_c_nd

    def createNode(self, name, node_name=None, move_to_cursor=True,
                   move_good_pos=False, move_to_vec=[False, [0, 0]]):

        if self.sel_c_nd > 0:
            move_to_cursor = False
            pos = self.sel_nd[0].position()
            pos[1] -= 1
            move_to_vec = [True, pos]
        try:
            node = self.net.createNode(name, node_name)
            if move_to_cursor:
                self.moveToCursor(node)
                move_good_pos = move_to_vec[0] = False
            elif move_good_pos:
                self.moveGoodPos(node)
                move_to_cursor = move_to_vec[0] = False
            elif move_to_vec[0]:
                self.moveToVec(node, move_to_vec[1])
                move_good_pos = move_to_cursor = False

            return node

        except hou.OperationFailed:
            print('Невозможно сотворить тут')
            return exit()

    def moveGoodPos(self, node):
        node.moveToGoodPosition()

    def moveToCursor(self, node):

        cursor = self.editor.cursorPosition()
        cursor[0] = round((cursor[0]) + 0.5) - 0.5
        cursor[1] = round((cursor[1]) + 0.85) - 1.15
        node.setPosition(cursor)

    def moveToVec(self, node, vec):

        try:
            node.setPosition(hou.Vector2(vec))
        except TypeError:
            print('Переменная не типа hou.Vector2')

    def nearestNeib(self, node):

        min_dist = 5 * 10**5
        nodes = self.child
        main_pos = node.position()
        for node in nodes:
            pos = node.position()
            dist = main_pos.distanceTo(pos)
            if ((dist < min_dist) and (main_pos != pos)
                    and (len(node.inputNames()) > 0)):
                min_dist = dist
                best = node
        return best

    def connectOneNearest(self, node, len_sel=0):

        if len_sel == 0:
            if len(node.inputNames()) == 0:
                return exit()
            if len(self.child) == 0:
                print('node not search to connect')
                return exit()

            nearNode = self.nearestNeib(node)
            node.setInput(0, nearNode)
        else:
            if len(node.inputNames()) == 0:
                return exit()
            if len(self.child) == 0:
                print('node not search to connect')
                return exit()
            nearNode = self.selNearArray(node, self.sel_nd)
            node.setInput(0, nearNode)

        return nearNode

    def selNearArray(self, node, array):
        import numpy as np

        distances = []
        main_pos = node.position()
        for n in array:
            pos_n = n.position()
            if n != node and len(node.inputNames()) > 0 and main_pos != pos_n:
                distances.append([main_pos.distanceTo(pos_n), n])
        nodes = np.array(distances)
        nodis = np.sort(nodes[::, 0])

        return nodes[np.where(nodes[:, 0] == nodis[0])][0][1]

    def nearestNeibs(self, node):

        distances = []
        main_pos = node.position()
        for n in self.child:
            pos_n = n.position()
            if n != node and len(node.inputNames()) > 0 and main_pos != pos_n:
                distances.append([main_pos.distanceTo(pos_n), n])

        return distances

    def connectAllNearest(self, node, sort_dist=False):
        import numpy as np

        if len(node.inputNames()) == 0:
            return exit()
        elif len(self.sel_nd) > 0:
            connectAllSelect(node, spare=True)
        elif len(self.child) == 1:
            print('node not search')
        elif len(self.child) - 1 > len(node.inputNames()):
            nodes = self.nearestNeibs(node)
            nodes = np.array(nodes)
            print('input < selected node. use spare')
            for k, nd in enumerate(nodes):
                if nd[1].position() == node.position():
                    continue
                else:
                    try:
                        if k < len(nd[1].inputNames()):
                            node.setInput(k, nd[1])
                        else:
                            self.connectAcrossSpare(node, nodes[k:, 1])
                    except hou.OperationFailed:
                        print('не все ноды имеет выходы')
        else:
            self.connectOneNearest(node)

    def connectAcrossSpare(self, node, c_nodes):

        for k, i in enumerate(c_nodes):
            tmp = hou.StringParmTemplate(
                name='spare_input%s' % (k),
                label='spare_input%s' % (k),
                num_components=1,
                string_type=hou.stringParmType.NodeReference)
            node.addSpareParmTuple(tmp)
            node.setParms({'spare_input%s' % (k): str(i.path())})

    def selectActions(self):
        buttons = ("Connect all", "Create each", "Cancel")
        selected_button = hou.ui.displayCustomConfirmation(
            "Count select node > count creating node input",
            suppress=hou.confirmType.TopCookSave, buttons=buttons)
        if selected_button == 0:
            buttons1 = ("Spare", "Merge", "Cancel")
            selected_button1 = hou.ui.displayCustomConfirmation(
                "Select type connect",
                suppress=hou.confirmType.TopCookSave, buttons=buttons1)
            if selected_button1 == 0:
                spare = True
                merge = False
                much_cr = False
            elif selected_button1 == 1:
                spare = False
                merge = True
                much_cr = False
            else:
                exit()

        elif selected_button == 1:
            spare = False
            merge = False
            much_cr = True
        elif selected_button == 2:
            exit()

        return spare, merge, much_cr

    def getDownerNode(self, arr_node):
        min_height = 9999999999
        for i in arr_node:
            if i.position()[1] < min_height:
                min_height = i.position()[1]
                downer_node = i

        return downer_node

    def connectAllSelect(self, node, much_cr=True,
                         spare=False, merge=False, user=False):
        import numpy as np

        def setCN(cur_nd, nd=False, node=None):
            if cur_nd not in self.searchByName('__Ddots__'):
                tmp = self.createNode(
                    node_type, node_name=node_name,
                    move_to_cursor=False)
                self.destroyMove(cur_nd, delete=False, dir=-1, node=node)
                if nd:
                    try:
                        node.destroy()
                    except hou.ObjectWasDeleted:
                        pass

                to_cn = [i for i in cur_nd.outputs()]
                try:
                    del to_cn[to_cn.index(tmp)]
                except ValueError:
                    pass

                for i in to_cn:
                    if len(i.inputNames()) == 1:
                        i.setInput(self.getNInput(cur_nd, i), tmp)
                    else:
                        if self.getNInput(cur_nd, i) != None:
                            i.setInput(self.getNInput(cur_nd, i), tmp)
                tmp.setInput(0, cur_nd)

                return tmp
            else:
                self.destroyMove(cur_nd, delete=False, dir=-1, node=node)

        if user:
            spare, merge, much_cr = self.selectActions()
        node_type = node.type().name()
        node_name = node.name()
        if len(node.inputNames()) == 0:
            return exit()
        if len(self.child) == 0:
            return -1
        if self.sel_c_nd == 0:
            self.connectOneNearest(node)
            return 1
        if self.sel_c_nd > len(node.inputNames()):
            if much_cr:
                for nd in self.sel_nd:
                    if nd is node:
                        setCN(nd, True, node)
                    elif len(nd.outputs()) == 0:
                        new_nd = setCN(nd, True, node)
                        if new_nd:
                            pos = nd.position()
                            pos[1] -= 1
                            self.moveToVec(new_nd, pos)
                    elif len(nd.outputs()) == 1:
                        new_nd = setCN(nd, True, node)
                        if new_nd:
                            pos = nd.position()
                            pos[1] -= 1
                            self.moveToVec(new_nd, pos)
                    else:
                        new_nd = setCN(nd, True, node)
                        if new_nd:
                            pos = nd.position()
                            pos[1] -= 1
                            self.moveToVec(new_nd, pos)
            elif spare:
                nodes = self.nearestNeibs(node, self.sel_nd)
                nodes = np.array(nodes)
                nodes = [nodes[i][1] for i in np.argsort(nodes[:, 0])]
                for k, toCn in enumerate(nodes):
                    if k > len(node.inputNames()) - 1:
                        tmp = hou.StringParmTemplate(
                            name='spare_input%s' % (k),
                            label='spare_input%s' % (k),
                            num_components=1,
                            string_type=hou.stringParmType.NodeReference)
                        node.addSpareParmTuple(tmp)
                        node.setParms(
                            {'spare_input%s' % (k): str(toCn.path())}
                        )
                    else:
                        node.setInput(k, toCn)
            elif merge:
                try:
                    merge = self.net.createNode('merge')
                    self.moveToCursor(merge)
                    pos = merge.position()
                    pos[1] -= 1
                    self.moveToVec(node, pos)
                except hou.OperationFailed:
                    print('Невозможно сотворить тут')
                    return -1
                for k, nd in enumerate(self.sel_nd):
                    merge.setInput(k, nd)
                node.setInput(0, merge)
            else:
                for i in range(self.sel_c_nd // len(node.inputNames()) + 1):
                    tmp = self.net.createNode(
                        node.type().name(), node_name=node.name())
                    pos = self.getDownerNode(
                        self.sel_nd[
                            len(node.inputNames()) * i: len(node.inputNames())
                            + len(node.inputNames()) * i]).position()
                    pos[1] -= 1
                    self.moveToVec(tmp, pos)
                    for k, j in enumerate(
                        self.sel_nd[
                            len(node.inputNames()) * i: len(node.inputNames())
                            + len(node.inputNames()) * i]):
                        tmp.setInput(k, j)
                node.destroy()
        elif self.sel_c_nd <= len(node.inputNames()):
            if self.sel_c_nd == 1:
                setCN(self.sel_nd[0], True, node)
            else:
                for k, toCn in enumerate(self.sel_nd):
                    node.setInput(k, toCn)

        elif self.sel_c_nd > 0 and not merge and not spare:
            try:
                for k, toCn in enumerate(self.sel_nd):
                    node.setInput(k, toCn)
            except hou.InvalidInput:
                print('input < selected node. use spare')
                self.connectAllSelect(node, spare=True)
        to_swap = self.searchByName('__Ddots__')
        for i in to_swap:
            self.swapNodeToDot(i)

    def splitToGroup(self, node):
        pos = node.position()
        dts = self.getNetDots(node)
        upper = []
        downer = []
        left = []
        right = []
        for nd in self.child:
            if nd.position()[1] > pos[1]:
                upper.append(nd)
                if nd.position()[0] < pos[0]:
                    left.append(nd)
                elif nd.position()[0] > pos[0]:
                    right.append(nd)
            elif nd.position()[1] <= pos[1]:
                downer.append(nd)
                if nd.position()[0] > pos[0]:
                    right.append(nd)
                elif nd.position()[0] <= pos[0]:
                    left.append(nd)
        for dt in dts:
            if dt.position()[1] > pos[1]:
                upper.append(dt)
                if dt.position()[0] < pos[0]:
                    left.append(dt)
                elif dt.position()[0] > pos[0]:
                    right.append(dt)
            elif dt.position()[1] <= pos[1]:
                downer.append(dt)
                if dt.position()[0] > pos[0]:
                    right.append(dt)
                elif dt.position()[0] <= pos[0]:
                    left.append(dt)
        return upper, downer, left, right

    def moveNodes(self, node, dir=['down', ['down']], value=[0, 1]):

        def get_dir(value):

            m_d = m_u = m_l = m_r = False
            if dir[1][0] == 'down':
                m_d = True
            elif dir[1][0] == 'up':
                m_u = True
                value[1] *= -1
            elif dir[1][0] == 'left':
                m_l = True
                value[0] *= -1
            elif dir[1][0] == 'right':
                m_r = True
            elif dir[1][1] == 'down':
                m_d = True
            elif dir[1][1] == 'up':
                m_u = True
                value[1] *= -1
            elif dir[1][1] == 'left':
                m_l = True
                value[0] *= -1
            elif dir[1][1] == 'right':
                m_r = True
            return m_u, m_r, m_l, m_d, value

        def get_arr():
            upper, downer, left, right = self.splitToGroup(node)
            if dir[0] == 'down':
                arr = downer
            elif dir[0] == 'up':
                arr = upper
            elif dir[0] == 'left':
                arr = left
            elif dir[0] == 'right':
                arr = right
            return arr

        def dirMove(_arr, value, _dir):
            if len(_dir[0]) == 1 and len(_dir[1]) == 0:
                for node in _arr:
                    pos = node.position()
                    pos[1] -= value[1]
                    node.setPosition(pos)
            elif len(_dir[1]) == 1 and len(_dir[0]) == 0:
                for node in _arr:
                    pos = node.position()
                    pos[0] -= value[0]
                    node.setPosition(pos)
            elif len(_dir[1]) == 1 and len(_dir[1]) == 1:
                for node in _arr:
                    pos = node.position()
                    pos[0] -= value[0]
                    node.setPosition(pos)

        m_u, m_r, m_l, m_d, value = get_dir(value)
        arr = get_arr()
        dir = [[i for i in [m_d, m_u] if i],
               [i for i in [m_l, m_r] if i]]
        dirMove(arr, value, dir)

    def getNetDots(self, arr=None):
        (self.sel_nd, self.editor, self.cursor,
         self.net, self.child, self.sel_c_nd) = self.update()
        if not arr:
            sp_dt = hou.node(self.net.path()).networkDots()
        else:
            sp_dt = []
            for i in arr:
                if isinstance(i, hou.NetworkDot):
                    sp_dt.append(i)
        return sp_dt

    def refCopy(self, node):

        fr = node
        to = self.createNode(fr.type().name())
        parm = {}
        for i in fr.parms():
            parm['%s' % (i.name())] = i.getReferencedParm()
        to.setParms(parm)
        to.setComment('Referenced from %s' % (fr.name()))
        to.setGenericFlag(hou.nodeFlag.DisplayComment, True)

        return to

    def flags(self, node, template=True, selected=True,
              display=True, render=True):

        for n in self.child:
            try:
                if template:
                    n.setTemplateFlag(0)
                if selected:
                    n.setSelected(0)
                if render:
                    n.setRenderFlag(0)
                if display:
                    n.setDisplayFlag(0)
                n.setSelectableTemplateFlag(0)
            except BaseException:
                pass
        try:
            if selected:
                node.setSelected(1)
            if display:
                node.setDisplayFlag(1)
            if render:
                node.setRenderFlag(1)
            if template:
                node.setTemplateFlag(1)
            node.setSelectableTemplateFlag(1)
        except BaseException:
            pass

    def setParms(self, node, nameParms, value):

        try:
            if not node.parm(nameParms):
                try:
                    node.setParms({'%s' % (nameParms): value})
                except TypeError:
                    print('Передаваемый параметр не совпадает по типу')
            else:
                print('parametr not found')
        except AttributeError:
            print('Переменная node не является типом hou.Node')

    def addSpareInput(self, node, count=1, names=[]):

        if len(names) == 0:
            for i in range(count):
                tmp = hou.StringParmTemplate(
                    name='spare_input%s' % (i),
                    label='spare_input%s' % (i),
                    num_components=1,
                    string_type=hou.stringParmType.NodeReference)
                node.addSpareParmTuple(tmp)
        else:
            if count < len(names):
                names = names[:count]
            for i in range(count):
                if len(names) >= i:
                    tmp = hou.StringParmTemplate(
                        name='%s' % (names[i]),
                        label='%s' % (names[i]),
                        num_components=1,
                        string_type=hou.stringParmType.NodeReference)
                    node.addSpareParmTuple(tmp)
                elif len(names) < i:
                    tmp = hou.StringParmTemplate(
                        name='spare_input%s' % (i),
                        label='spare_input%s' % (i),
                        num_components=1,
                        string_type=hou.stringParmType.NodeReference)
                    node.addSpareParmTuple(tmp)

    def insertBetween(self, node):

        up_min = 5 ** 10
        for nd in self.child:
            pos = nd.position()
            if ((self.cursor[1] - pos[1])**2)**0.5 < up_min:
                if pos[1] >= self.cursor[1]:  # up
                    up_min = ((self.cursor[1] - pos[1])**2)**0.5
                    up = nd
        try:
            if isinstance(up, hou.Node):
                self.moveNodes(node)
                nodes = up.outputs()
                if len(nodes) > 0:
                    node.setInput(0, up)
                    for n in nodes:
                        n.setInput(0, node)
                else:
                    self.connectOneNearest(node)

        except NameError:
            print('not search upper node')

    def getNInput(self, par, child):
        if (isinstance(par, hou.Node)
                and isinstance(child, hou.Node)):
            for k, inp in enumerate(
                [i for i in [child.inputConnections()[j].inputItem()
                             for j in range(
                    len(child.inputConnections()))]]
            ):
                if inp == par:
                    return k
                elif isinstance(inp, hou.NetworkDot):
                    return 0

        else:
            return 0

    def swapDotToNode(self, dot):
        outputs = [i for i in [dot.outputConnections()[j].outputItem()
                               for j in range(len(dot.outputConnections()))]]
        pos = dot.position()
        tmp = self.createNode('null', node_name='__Ddots__',
                              move_to_cursor=False, move_to_vec=[False, pos])
        tmp.setInput(0, dot.inputConnections()[0].inputItem())
        for i in outputs:
            i.setInput(self.getNInput(dot.inputConnections()
                                      [0].inputItem(), i), tmp)
        self.moveToVec(tmp, pos)
        try:
            self.sel_nd[self.sel_nd.index(dot)] = tmp
        except ValueError:
            pass
        dot.destroy()

        return tmp

    def swapNodeToDot(self, node):
        outputs = [i for i in [node.outputConnections()[j].outputItem()
                               for j in range(len(node.outputConnections()))]]
        pos = node.position()
        tmp = self.net.createNetworkDot()
        tmp.setInput(0, node.inputConnections()[0].inputItem())
        for i in outputs:
            i.setInput(self.getNInput(node, i), tmp)
        self.moveToVec(tmp, pos)
        node.destroy()
        return tmp

    def destroyMove(self, par, delete=True, dir=1, node=None, up=True):
        if up:
            (self.sel_nd, self.editor, self.cursor,
             self.net, self.child, self.sel_c_nd) = self.update()
        child = [i for i in self.child]
        if node:
            try:
                del child[child.index(node)]
            except hou.ObjectWasDeleted:
                pass
        d = self.sortByHeight(child, False)
        for k, v in d.items():
            if par in v:
                t = int(k)
        childs = []
        move = []
        for i in range(t, -1, -1):
            if len(childs) == 0:
                for j in d['%s' % (i)]:
                    if isinstance(j[0], hou.NetworkDot):
                        dot = self.swapDotToNode(j[0])
                        if dot in par.outputs():
                            if abs(dot.position()[1]
                                   - (par.position()[1])) < abs(dir) + 0.5:
                                childs.append(dot)
                                move.append(dot)
                    else:
                        if j[0] in par.outputs():
                            if abs(j[0].position()[1]
                                   - (par.position()[1])) < abs(dir) + 0.5:
                                move.append(j[0])
                                childs.append(j[0])

            elif len(childs) > 0:
                for j in d['%s' % (i)]:
                    if isinstance(j[0], hou.NetworkDot):
                        dot = self.swapDotToNode(j[0])
                        for k in childs:
                            if dot in k.outputs():
                                if abs(dot.position()[1]
                                       - (k.position()[1])) < abs(dir) + 0.5:
                                    move.append(dot)
                                    childs.append(dot)
                    else:
                        for k in childs:
                            if j[0] in k.outputs():
                                if abs(j[0].position()[1]
                                       - (k.position()[1])) < abs(dir) + 0.5:
                                    move.append(j[0])
                                    childs.append(j[0])

        for i in childs:
            pos = i.position()
            pos[1] += dir
            self.moveToVec(i, pos)
        if delete:
            par.destroy()

    def sortByHeight(self, arr, on=True):
        import numpy as np
        evol = {}
        tmp = np.array([['n', 'd'], ])
        for nd in arr:
            tmp1 = np.array([[nd, (nd.position()[1])], ])
            tmp = np.vstack((tmp, tmp1))
        if on:
            pts = self.getNetDots(arr)
        else:
            pts = self.getNetDots()
        for pt in pts:
            tmp1 = np.array([[pt, (pt.position()[1])], ])
            tmp = np.vstack((tmp, tmp1))
        tmp = tmp[1:]
        h = np.sort(tmp[:, 1])
        for k, i in enumerate(np.unique(h)):
            evol['%s' % (k)] = tmp[np.where(tmp[:, 1] == i)]

        return evol

    def searchByName(self, name, space=None):
        (self.sel_nd, self.editor, self.cursor,
         self.net, self.child, self.sel_c_nd) = self.update()
        arr = []
        if space == None:
            for i in self.child:
                if i.name().find(name) != -1:
                    arr.append(i)
        return arr

    def recon(self, tar1_in, tar1_ot, tar2_in, tar2_ot, tar1, tar2):
        for i in tar1_in:
            try:
                if i[0][0] != i[2]:
                    i[0][0].setInput(i[1], i[2])
                else:
                    if i[2] == tar1:
                        tar2.setInput(i[1], tar1)
                    elif i[2] == tar2:
                        tar1.setInput(i[1], tar2)
            except hou.InvalidInput:
                print('didn`t search input')
        for i in tar2_in:
            try:
                if i[0][0] != i[2]:
                    i[0][0].setInput(i[1], i[2])
            except hou.InvalidInput:
                print('didn`t search input')
        for i in tar1_ot:
            try:
                if i[0][0] != i[2]:
                    i[0][0].setInput(i[1], i[2])
                else:
                    if i[2] == tar1:
                        tar2.setInput(i[1], tar1)
                    elif i[2] == tar2:
                        tar1.setInput(i[1], tar2)
            except hou.InvalidInput:
                print('didn`t search input')
        for i in tar2_ot:
            try:
                if i[0][0] != i[2]:
                    i[0][0].setInput(i[1], i[2])
                else:
                    if i[2] == tar1:
                        tar2.setInput(i[1], tar1)
                    elif i[2] == tar2:
                        tar1.setInput(i[1], tar2)
            except hou.InvalidInput:
                print('didn`t search input')

    def swap(self):
        if self.sel_c_nd == 2:
            conect = {}
            tar1 = self.sel_nd[0]
            tar2 = self.sel_nd[1]
            tmp = self.sel_nd[0].position()
            conect[tar1.name()] = [
                [i for i in [tar1.outputConnections()[j].outputItem()
                             for j in range(len(tar1.outputConnections()))]],
                [i for i in [tar1.inputConnections()[j].inputItem()
                             for j in range(len(tar1.inputConnections()))]]]
            conect[tar2.name()] = [
                [i for i in [tar2.outputConnections()[j].outputItem()
                             for j in range(len(tar2.outputConnections()))]],
                [i for i in [tar2.inputConnections()[j].inputItem()
                             for j in range(len(tar2.inputConnections()))]]]
            self.moveToVec(tar1, tar2.position())
            self.moveToVec(tar2, tmp)
            tar_1_in = []
            tar_1_ot = []
            tar_2_in = []
            tar_2_ot = []
            for i in conect[tar1.name()][0]:
                tar_1_ot.append([[i], self.getNInput(tar1, i), tar2])
            for i in conect[tar1.name()][1]:
                tar_1_in.append([[tar2], self.getNInput(i, tar1), i])
            for i in conect[tar2.name()][0]:
                tar_2_ot.append([[i], self.getNInput(tar2, i), tar1])
            for i in conect[tar2.name()][1]:
                tar_2_in.append([[tar1], self.getNInput(i, tar2), i])
            self.recon(tar_1_in, tar_1_ot, tar_2_in, tar_2_ot, tar1, tar2)

        else:
            print('Select two nodes')

    def swapOnRef(self):
        head = self.sel_nd[0]
        to_swap = self.sel_nd[1:]
        for i in to_swap:
            pos = i.position()
            tmp = self.refCopy(head)
            self.moveToVec(tmp, pos)
            i.destroy()

    def calcDist(self, node_a, node_b):
        height = node_a.position()[1] - (node_b.position()[1] - 1)
        weight = node_a.position()[0] - (node_b.position()[0])

        return height, weight

    def getHeightClipboard(self):
        self.net.pasteItemsFromClipboard(self.sel_nd[0].position())
        mas_copy_nodes = hou.selectedItems()
        arr_nds = self.sortByHeight(mas_copy_nodes)
        head = arr_nds[str(len(arr_nds) - 1)][0][0]
        downer = self.getDownerNode(mas_copy_nodes)
        height = abs(head.position()[1] - downer.position()[1])
        for i in mas_copy_nodes:
            i.destroy()

        return height + 1

    def pasteFromClipboard(self, node):
        height = self.getHeightClipboard()
        self.destroyMove(node, dir=- int(height), delete=False)
        self.net.pasteItemsFromClipboard(self.sel_nd[0].position())
        mas_copy_nodes = hou.selectedItems()
        arr_nds = self.sortByHeight(mas_copy_nodes)
        head = arr_nds[str(len(arr_nds) - 1)][0][0]
        y, x = self.calcDist(head, node)
        head.setInput(0, node)
        visit = []
        for k, v in arr_nds.items():
            for j in v:
                if j[0] not in visit:
                    pos = j[0].position()
                    pos[0] -= x - 1
                    pos[1] -= y
                    self.moveToVec(j[0], pos)
                    visit.append(j[0])

    def copyAllWire(self):
        for i in self.sel_nd:
            self.pasteFromClipboard(i)

    def color(self):
        LGBT = [
            [1, 0, 0],
            [1, 0.3, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0.5, 0, 1]
        ]
        import random
        if len(self.sel_nd) % 6 == 0:
            for k, i in enumerate(self.sel_nd):
                i.setColor(hou.Color(LGBT[k % 6]))
        else:
            for i in self.sel_nd:
                i.setColor(hou.Color(random.random(),
                                     random.random(), random.random()))

    def delete_wire(self, node_a, node_b):
        for k, i in enumerate(node_b.inputs()):
            if i == node_a:
                node_b.setInput(k, None)

    def delete(self, mouse=False):
        (self.sel_nd, self.editor, self.cursor,
         self.net, self.child, self.sel_c_nd) = self.update()
        wire = hou.selectedConnections()
        nodes_dots = [i for i in hou.selectedItems()]
        [nodes_dots.append(i) for i in self.getNetDots()]
        if mouse:
            for i in self.child:
                if(abs(i.position()[0] - self.cursor[0]) < 0.6
                        and abs(i.position()[1] - self.cursor[1]) < 0.6):
                    nodes_dots.append(i)
        for i in nodes_dots:
            i.destroy()
        for i in wire:
            self.delete_wire(i.inputNode(), i.outputNode())

    def moveNodeKeyboard(self):
        import keyboard
        from threading import Thread
        import time

        def threads():
            while True:
                if keyboard.is_pressed('q'):
                    exit()
                elif (keyboard.is_pressed('up')
                      and keyboard.is_pressed('alt')):
                    nodes = hou.selectedNodes()
                    for node in nodes:
                        pos = node.position()
                        pos[1] += 1
                        node.setPosition(pos)
                    time.sleep(0.1)
                elif (keyboard.is_pressed('down')
                      and keyboard.is_pressed('alt')):
                    nodes = hou.selectedNodes()
                    for node in nodes:
                        pos = node.position()
                        pos[1] -= 1
                        node.setPosition(pos)
                    time.sleep(0.1)
                elif (keyboard.is_pressed('left')
                      and keyboard.is_pressed('alt')):
                    nodes = hou.selectedNodes()
                    for node in nodes:
                        pos = node.position()
                        pos[0] -= 1
                        node.setPosition(pos)
                    time.sleep(0.1)
                elif (keyboard.is_pressed('right')
                      and keyboard.is_pressed('alt')):
                    nodes = hou.selectedNodes()
                    for node in nodes:
                        pos = node.position()
                        pos[0] += 1
                        node.setPosition(pos)
                    time.sleep(0.1)
                else:
                    time.sleep(0.1)

        th = Thread(target=threads)
        th.start()

    def deleteRef(self, node):
        for parm in node.parms():
            parm.deleteAllKeyframes()
        node.setComment(None)

    def deleteALLRef(self):
        for node in self.sel_nd:
            self.deleteRef(node)

    def copyToBroadwise(self, node):
        button_idx, values = hou.ui.readMultiInput(
            "Set count and dist for copy", ("Count", "Distance"),
            initial_contents=(str(1), str(1)),
            title="Set parametrs for for copy",
            buttons=("Copy", "Copy with reference", "Cancel"),
        )
        if button_idx == 0:
            for i in range(1, int(values[0]) + 1):
                tmp = self.createNode(node.type().name(),
                                      node_name=node.name()
                                      )
                pos = node.position()
                pos[0] += i * int(values[1])
                self.moveToVec(tmp, pos)
        elif button_idx == 1:
            for i in range(1, int(values[0]) + 1):
                tmp = self.refCopy(node)
                pos = node.position()
                pos[0] += i * int(values[1])
                self.moveToVec(tmp, pos)
        else:
            exit()


hk = ObjContext()
