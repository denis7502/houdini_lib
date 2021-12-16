# houdini_lib
Custom houdini lib for obj context
Import
---------------------------------------------------
Необходимо создать папку script в директории houdini.
Пример пути:
C:\Users\123\Documents\houdini18.5
В ней можно создать свою иерархию папок в конечную папку помещаем файл с библиотекой
Пример пути:
C:\Users\123\Documents\houdini18.5\scripts\python\hvdk\lib
Для импорта внутри гудини необходимо импортировать следующее
Пример импорта:
from hvdk.lib import hvdk_lib as hvdk
где,
	hvdk, lib - папки по пути к файлу
	as hvdk - определяет имя импортированого модуля, можно не использовать

Последний шаг определение класс для доступа ко всем методам
Пример для вышеприведенных строк:
hk = hvdk.hk


Теперь для вызова функции необходимо сделать следующий вызов:
hk.name_method()


------------------------------------------------------


Список методов:


update() - обновление глобальных параметров возвращает выбранные ноды, нетворк, объект курсора, все ноды в нетворке, кол-во выбранных нод

createNode(name, node_name=None, move_to_cursor=True, move_good_pos=False, move_to_vec=[False, [0, 0]]) - создаёт ноду указаную в параметре name с указанным именем в node_name

moveGoodPos(node) - перемещает ноду в "хорошую" позицию

moveToCursor(node) - перемещает ноду в позицую курсору

moveToVec(node, vec) - перемещает ноду в выбранную точку

nearestNeib(node) - находит ближайшую ноду к переданной

connectOneNearest(node, len_sel=0) - подключает ноду к одной ближайшей

selNearArray(node, array) - созадёт массив нод в порядке удаления от ноды

nearestNeibs(node) - создаёт массив нод и расстояний до них для всего пр-ва нетворка

connectAllNearest(node, sort_dist=False) - подключает все ближайшие ноды

connectAcrossSpare(node, c_nodes) - подключение через Spare input

selectActions() - рабочая функция с реализацией выбора методы подключения

getDownerNode(arr_node) - возвращает ноду находящююся ниже всех в массиве

connectAllSelect(node, much_cr=True, spare=False, merge=False, user=False) - функция реализующая разные подключения нод

splitToGroup(node) - рабочая функция (не используется), разбивает пр-во на массивы нод находящихся слева, справа, снизу, сверху

moveNodes(node, dir=['down', ['down']], value=[0, 1]) - рабочая функция (не используется), перемещает группу в выбранном направлении и на заданную величину

getNetDots(arr=None) - возвращает все точки в нетворке или в массиве

refCopy(node) - создает референсую ноду для выбранной

flags(node, template=True, selected=True, display=True, render=True) -  переключает флаги на выбранной ноде

setParms(node, nameParms, value) - устанавливает параметр у ноды в заданное значение

addSpareInput(node, count=1, names=[]) - рабочая функция (не используется), добавляет Spare input к ноде

insertBetween(node) - рабочая функция (не используется), вставляет ноду между 2-мя выбранными

getNInput(par, child) - возвращает номер входа в которую конектится 1-ая во второй

swapDotToNode(dot) - заменяет точку на ноду

swapNodeToDot(node) - заменяет ноду на точку

destroyMove(par, delete=True, dir=1, node=None, up=True) - удаляет ноду и смещает в напралвении 

sortByHeight(arr, on=True) - возвращает словарь с отсортированными по высоте ноды

searchByName(name, space=None) -  возвращет ноды в названии которых есть name

recon(tar1_in, tar1_ot, tar2_in, tar2_ot, tar1, tar2) - переподключает ноды между собой

swap() -  меняет местами ноды вместе с подключениями

swapOnRef() - заменяет выбранный ноды на референс первой выбранной ноды

calcDist(node_a, node_b) -  считает дистанцию по x,y для нод

getHeightClipboard() - возвращает разницу по высоте между самой верхней и самой нижней нодой

pasteFromClipboard(node) - подключает скопированые ноды к выбранной

copyAllWire() - вставляет из буффера обмена к каждой выбранной ноде

color() - разукрашивает все ноды в рандомный цвет

delete_wire(node_a, node_b) - удаляет связи между нодами

delete(mouse=False) - удаляет все выбранные объекты

moveNodeKeyboard() - перемещение ноды при помощи клавиатуры

deleteRef(node) - удаляет референс у ноды

deleteALLRef() - удаляет референс у всех нод

copyToBroadwise(node) - вставка нод в ширь



------------------------------------------------------------------------


update()
	Возвращает обновленные глобальные параметры.
	Выбранные ноды - массив типа hou.Node
	Нетворк - ссылка на Нетворк типа hou.NetworkEditor
	Позиция курсора - двумерный вектор типа hou.Vector2
	Нода - нода текущего пр-ва типа hou.Node
	Список всех ноды в текущем пр-ве tuple типа hou.Node


createNode(name, node_name=None, move_to_cursor=True, move_good_pos=False, move_to_vec=[False, [0, 0]])
	Созадаёт ноду с указаными параметрами
	name(str) - имя ноды в пр-ве Houdini
		Например:
				'xform' - создаст ноду трансформ
	node_name(str) - задаёт именя ноды, при None задаст стандартное имя
	move_to_cursor(bool) - True при создании переместит ноду в позицию курсора
	move_good_pos(bool) - True перемести ноду в "хорошую" позицию
	move_to_vec(list(bool, [x,y])) - True переместит в указанную следом точку


moveGoodPos(node)
	Перемещает ноду в "хорошую позицию"
	node(hou.Node) - нода которую надо переместить


moveToCursor(node)
	Перемещает ноду в позицию курсора
	node(hou.Node) - нода которую надо переместить


moveToVec(node, vec)
	Перемещает ноду в заданную позицию
	node(hou.Node) - нода которую надо переместить
	vec(list([x,y])) - позиция в которую перемещается нода


nearestNeib(node)
	Возвращает ближайшую ноду к выбранной
	node(hou.Node) - нода поиск около которой осуществляется поиск


connectOneNearest(node, len_sel = 0)
	Подключает к выбранной ноде ближайшую или ближайшую из списка
	node(hou.Node) - нода к которой надо подключить ближайшую
	len_sel(int) - если не 0, то поиск ближайшей ноды среди нод в массиве выбранных нод


selNearArray(node,array)
	Возвращает numpy массив нод в порядке возрастание расстояний от ноды
	node(hou.Node) - нода от которой считается дистанция
	array(list) - список нод для сортировки по расстоянию


nearestNeibs(node)
	Тоже самое что nearestNeib, в качестве массива передается текущее пр-во Нетворка



connectAllNearest(node, sort_dist=False)
	Подключает все ближайшие ноды, если нод больше, то подключает через Spare Input
	node(hou.Node) - нода к которой подключается всё остальное
	sort_dits - Если True, то подключается попорядку удаленности


connectAcrossSpare(node, c_nodes)
	Подключение нод через Spare Input к первой
	node(hou.Node) - нод к которой подключается
	c_nodes(list(hou.Node)) - список нод для подключения


selectActions()
	Рабочая функция, можно использовать как пример


getDownerNode(arr_node)
	Возвращает нижнюю ноду в списке
	arr_node(list(hou.Node)) - список нод для поиска нижней


connectAllSelect(node, much_cr=True, spare=False, merge=False, user=False)
	Подключение нод в разных ситуациях
	node(hou.Node) - нода которую надо подключить
	much_cr(bool) - если True, и выбрано множество нод, создаёт копию переданной ноды под каждой выбранной
	spare(bool) - если True подключение к переданной ноде через Spare Input
	merge(bool) - если True подключение через merge ноду в геометрическом контексте
	user(bool) - если True включает интерфейс для выбора подключения


splitToGroup(node)
	Рабочая функция, делит ноды на массив функции находящихся слева, справа, снизу, сверху


moveNodes(node, dir=['down', ['down']], value=[0, 1])
	Рабочая функци, перемещает выбранную группу в выбранном направлении


getNetDots(arr=None)
	Вовзвращает массив hou.NetworkDot находящихся в нетворке точек


refCopy(node)
	Создаёт референсую ноды переданной 
	node(hou.Node) - нода рефернс которой надо созадать


flags(node, template=True, selected=True, display=True, render=True)
	Убирает/устанавливает флаги со всех остальных нод и устанавливает/убирает на переданной


setParms(node, nameParms, value)
	Устанавливет переданный параметр переданное значении в выбранной ноде
	node(hou.Node) - нода для которой устанавливается параметр
	nameParms(str) - имя параметра в пр-ве houdini
	value(type(parms)) - значение которое необходимо установить, тип соответсвует типу параметра


addSpareInput(node, count=1, names=[])
	Рабочая функция, добавляет Spare Input к ноде


insertBetween(node)
	Вставку ноду, между другими нодами, рабочая функция


getNInput(par, child)
	Возвращает номер входа в ноде par, в который подключен child
	par(hou.Node) - нода вход в который необходимо определить
	child(hou.Node) -  подключаемая нода


swapDotToNode(dot)
	Заменяет точку на ноду
	dot(hou.NetworkDot) - точка для замены


swapNodeToDot(node)
	Заменяет ноду на точку
	node(hou.Node) - нода для замены


destroyMove(par, delete=True, dir=1, node=None, up=True)
	Удаляет ноду и смещает все дочерние ноды на dir в верх
	par(hou.Node) - нода для удаление
	delete(bool) - если False нода не удаляется
	dir(int) - величина смещения массива нод
	node(hou.node) - нода которую не надо перемещать
	up(bool) - если True, перед выполнение обновляет глобальные параметры


sortByHeight(arr, on=True)
	Возвращает словарь с отсортированными по высоте нодами
		Пример структуры:
			{1:'null1', 2:'null2'}
			null1 на уровень выше null2
	arr(list(hou.Node)) - список нод для сортировки
	on(bool) - если True включает точки в сортировку


searchByName(name, space=None)
	Возвращает список нод содержащих name в имени ноды
	name(str) - искомое имя
	space(hou.Node) - пр-во для поиска


recon(tar1_in, tar1_ot, tar2_in, tar2_ot, tar1, tar2)
	Переподключает входы и выходы из tar1 в tar2 и из tar2 в tar1
	tar1_in, tar2_in(list(hou.Node)) - список нод входящих в tar1 и tar2
	tar1_ot, tar2_ot(list(hou.Node)) - список нод выходящих в tar1 и tar2
	tar1, tar2 (hou.Node) - ноды для переподключения


swap()
	Меняет местами 2 выбранные ноды, если выбрано больше нод, то ошибка


swapOnRef()
	Заменяет все кроме первой выбранной ноды на референс первой ноды


calcDist(node_a, node_b)
	Сччитает расстояние по двум осям от а ноды до б ноды
	node_a(hou.Node) - нода от которой считается расстояние
	node_b(hou.Node) - нода до которой считается расстояние


getHeightClipboard()
	Вовзращает расстояние между самой верхней и самой нижней нодой в скопированных в буфер обмена нодах


pasteFromClipboard(node)
	Вставляет из буфера обмена и подключает к переданной ноде
	node(hou.Node) - нода для подключения


copyAllWire()
	Работает как pasteFromClipboard, для всез выбранных нод


color()
	Разукрашивает ноды в рандомные цвета


delete_wire(node_a, node_b)
	Удаляет wire между нодами а и б
	node_a (hou.Node)
	node_b(hou.Node)


delete(mouse=False)
	Удаляет все выбранные объекты
	mouse(bool) - если true, удаляет все ноды в небольшом расстоянии от положения курсора


moveNodeKeyboard()
	При активации перемещает ноды при помощи клавиатуры. ALT+down,up,right,left arrow. Для выхода q


deleteRef(node)
	Удаление референса у переданной ноды
	node(hou.Node) - нода для удаления зависимости


deleteALLRef()
	Работает как deleteRef, для всез выбранных но

copyToBroadwise(node)
	Вызывает пользовательский интерфейс для выбора кол-ва и дистанции между нодами для создания в ширь
	node(hou.Node) -  нода относительно которой идёт смещение вправо или влево
