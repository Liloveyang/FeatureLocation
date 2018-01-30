from Dataset import *
import os
from Util import *
import re

#数据预处理，主要是处理数据库中的各种数据
def processGoldensets(oldmethod):
    #找不到该方法
    delete =['org.gjt.sp.jedit.PluginJAR.jarCompare(String,String)',
             'org.gjt.sp.jedit.PluginJAR.loadDependencies(String)',
            'org.gjt.sp.jedit.pluginmgr.ManagePanel.PluginTableModel.toggleCurrentRow()',
             'org.gjt.sp.jedit.search.PatternSearchMatcher.isMatchingEOL()',
             'org.gjt.sp.jedit.search.SearchMatcher.isMatchingEOL()',
             'org.gjt.sp.jedit.buffer.JEditBuffer.getUndoManager()',
             'org.gjt.sp.jedit.buffer.UndoManager.bufferSaved()',
             'org.gjt.sp.jedit.textarea.Gutter.getFoldPainterName()',
             'org.gjt.sp.jedit.options.ShortcutsOptionPane.ShortcutsModel.resetFilter()',
             'org.gjt.sp.jedit.options.ShortcutsOptionPane.ShortcutsModel.setFilter(String)',
             'org.gjt.sp.jedit.options.ShortcutsOptionPane.ShortcutsModel.getFilteredBindingAt(int,int)',
             'org.gjt.sp.jedit.textarea.TextArea.scrollToCurrent()',
             'org.gjt.sp.jedit.bufferset.BufferSetManager.BufferSetClosed.init()',
             'org.gjt.sp.jedit.bufferset.BufferSet.finalize()',
             'org.gjt.sp.jedit.textarea.Gutter.getLineCount()', 'org.gjt.sp.jedit.pluginmgr.ManagePanel.KeyHandler.keyTyped(KeyEvent)',
             'org.gjt.sp.jedit.pluginmgr.ManagePanel.KeyHandler.keyPressed(KeyEvent)',
             'org.gjt.sp.jedit.pluginmgr.ManagePanel.KeyHandler.keyReleased(KeyEvent)',
             'org.gjt.sp.jedit.textarea.JEditTextArea.getSelectedText(Selection)',
                'org.gjt.sp.jedit.textarea.JEditTextArea.collapseFold()',
                'org.gjt.sp.jedit.textarea.JEditTextArea.collapseFold(int)',
                'org.gjt.sp.jedit.textarea.CircleFoldPainter.paintFoldEnd(Gutter,Graphics2D,int,int,int,int,JEditBuffer)',
                'org.gjt.sp.jedit.textarea.CircleFoldPainter.paintFoldMiddle(Gutter,Graphics2D,int,int,int,int,JEditBuffer)',
                'org.gjt.sp.jedit.textarea.CircleFoldPainter.paintFoldStart(Gutter,Graphics2D,int,int,boolean,int,int,JEditBuffer)',
             'org.gjt.sp.jedit.textarea.SquareFoldPainter.paintFoldEnd(Gutter,Graphics2D,int,int,int,int,JEditBuffer)',
             'org.gjt.sp.jedit.textarea.SquareFoldPainter.paintFoldStart(Gutter,Graphics2D,int,int,boolean,int,int,JEditBuffer)',
             'org.gjt.sp.jedit.textarea.SquareFoldPainter.paintFoldMiddle(Gutter,Graphics2D,int,int,int,int,JEditBuffer)'
             ]
    #需要进行更新的数组
    deprecated = ['org.gjt.sp.jedit.gui.StatusBar.MemoryStatus.getToolTipText()',
                  'org.gjt.sp.jedit.gui.StatusBar.MemoryStatus.paintComponent(Graphics)',
                  'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(Window,String)',
                  'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(Window,Container,String)',
                  'org.gjt.sp.jedit.GUIUtilities.addSizeSaver(Window,String)',
                  'org.gjt.sp.jedit.GUIUtilities.addSizeSaver(Window,Container,String)',
                   'org.gjt.sp.jedit.PluginJAR.transitiveClosure(Set<String>,Set<String>)',
                  'org.gjt.sp.jedit.gui.FloatingWindowContainer.register(DockableWindowManager.Entry)',
                  'org.gjt.sp.jedit.textarea.TextArea.joinLines(Selection)',
                  'org.gjt.sp.jedit.Buffer.Buffer(String,boolean,boolean,Hashtable)',
                  'org.gjt.sp.jedit.jEdit.composeBufferPropsFromHistory(Hashtable,String)',
                  'org.gjt.sp.jedit.gui.OptionsDialog.selectPane(OptionGroup,String,List)',
                  'org.gjt.sp.jedit.syntax.ParserRule.createSpanRule(int,String,int,String,ParserRuleSet,byte,byte,boolean,boolean,boolean)',
                  'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(String,int,String,int,String,ParserRuleSet,byte,byte,boolean,boolean,boolean,boolean)',
                  'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(char,int,String,int,String,ParserRuleSet,byte,byte,boolean,boolean,boolean,boolean)',
                  'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(int,char[],String,int,String,ParserRuleSet,byte,byte,boolean,boolean,boolean,boolean)',
                  'org.gjt.sp.jedit.syntax.ParserRule.ParserRule(int,String,int,char[],Pattern,int,char[],ParserRuleSet,byte,byte)',
                  'org.gjt.sp.jedit.syntax.ParserRule.ParserRule(char[],int,int,char[],Pattern,int,char[],ParserRuleSet,byte,byte)',
                  'org.gjt.sp.jedit.syntax.TokenMarker.handleRule(ParserRule,boolean,boolean)',
                  'org.gjt.sp.jedit.textarea.Gutter.setFoldPainter(String)',
                  'org.gjt.sp.jedit.pluginmgr.ManagePanel.SaveButton.saveState(String,StringList)',
                  'org.gjt.sp.jedit.options.ShortcutsOptionPane.ShortcutsModel.ShortcutsModel(String,Vector<GrabKeyDialog.KeyBinding[]>)',
                  'org.gjt.sp.jedit.pluginmgr.InstallPanel.EntryCompare.compare(Object,Object)',
                  'org.gjt.sp.jedit.gui.FilePropertiesDialog.FilePropertiesDialog(View,VFSBrowser)',
                  'org.gjt.sp.jedit.bufferset.BufferSetManager.BufferSetClosed.BufferSetClosed(View,BufferSet)',
                  'org.gjt.sp.jedit.bufferset.BufferSetManager.BufferSetClosed.BufferSetClosed(EditPane,BufferSet)',
                  'org.gjt.sp.jedit.bufferset.BufferSet.BufferSet(Scope)',
                  'org.gjt.sp.jedit.bufferset.BufferSet.handleMessage(PropertiesChanged)',
                  'org.gjt.sp.jedit.bufferset.BufferSet.handleMessage(EBMessage)',
                  'org.gjt.sp.jedit.search.HyperSearchResults.HighlightingTree.appendString2html(StringBuffer,String)',
                  'org.gjt.sp.jedit.textarea.Gutter.setSelectonAreaEnabled(boolean)',
                  'org.gjt.sp.jedit.PluginJAR.load(boolean)',
                  'org.gjt.sp.jedit.TextUtilities.join(Collection,String)',
                  'org.gjt.sp.jedit.textarea.Anchor.preContentRemoved(int,int)',
                  'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(Frame,String)',
                  'org.gjt.sp.jedit.jEdit.finishStartup(boolean,boolean,String,String[])'
                  ]
    #与deprecated一一对应，将其更新为updated中的方法
    updated = ['org.gjt.sp.jedit.gui.statusbar.MemoryStatusWidgetFactory.MemoryStatus.getToolTipText()',
               'org.gjt.sp.jedit.gui.statusbar.MemoryStatusWidgetFactory.MemoryStatus.paintComponent(java.awt.Graphics)',
               'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(java.awt.Frame,java.awt.Container,java.lang.String)',
               'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(java.awt.Frame,java.awt.Container,java.lang.String)',
               'org.gjt.sp.jedit.GUIUtilities.addSizeSaver(java.awt.Frame,java.lang.String)',
               'org.gjt.sp.jedit.GUIUtilities.addSizeSaver(java.awt.Frame,java.awt.Container,java.lang.String)',
               'org.gjt.sp.jedit.PluginJAR.transitiveClosure(java.lang.String[],java.util.List<java.lang.String>)',
               'org.gjt.sp.jedit.gui.FloatingWindowContainer.register(org.gjt.sp.jedit.gui.DockableWindowManagerImpl.Entry)',
               'org.gjt.sp.jedit.textarea.TextArea.joinLines()',
               'org.gjt.sp.jedit.Buffer.Buffer(java.lang.String,boolean,boolean,java.util.Map)',
               'org.gjt.sp.jedit.jEdit.composeBufferPropsFromHistory(java.util.Map,java.lang.String)',
               'org.gjt.sp.jedit.gui.OptionsDialog.selectPane(org.gjt.sp.jedit.OptionGroup,java.lang.String,java.util.List<java.lang.Object>)',
               'org.gjt.sp.jedit.syntax.ParserRule.createSpanRule(int,java.lang.String,int,java.lang.String,org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,boolean,boolean,java.lang.String)',
               'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(java.lang.String,int,java.lang.String,int,java.lang.String,org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,boolean,boolean,boolean,java.lang.String)',
               'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(java.lang.String,int,java.lang.String,int,java.lang.String,org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,boolean,boolean,boolean,java.lang.String)',
               'org.gjt.sp.jedit.syntax.ParserRule.createRegexpSpanRule(int,char[],java.lang.String,int,java.lang.String,org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,boolean,boolean,boolean,java.lang.String)',
               'org.gjt.sp.jedit.syntax.ParserRule.ParserRule(int,java.lang.String,int,char[],java.util.regex.Pattern,int,char[],org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,java.lang.String)',
               'org.gjt.sp.jedit.syntax.ParserRule.ParserRule(char[],int,int,char[],java.util.regex.Pattern,int,char[],org.gjt.sp.jedit.syntax.ParserRuleSet,byte,byte,java.lang.String)',
               'org.gjt.sp.jedit.syntax.TokenMarker.handleRule(org.gjt.sp.jedit.syntax.ParserRule,boolean)',
               'org.gjt.sp.jedit.textarea.Gutter.setFoldPainter(org.gjt.sp.jedit.textarea.FoldPainter)',
               'org.gjt.sp.jedit.pluginmgr.ManagePanel.SaveButton.saveState(java.lang.String,java.util.List<org.gjt.sp.jedit.pluginmgr.ManagePanel.Entry>)',
               'org.gjt.sp.jedit.options.ShortcutsOptionPane.ShortcutsModel.ShortcutsModel(java.lang.String,java.util.List<org.gjt.sp.jedit.gui.GrabKeyDialog.KeyBinding[]>)',
               'org.gjt.sp.jedit.pluginmgr.InstallPanel.EntryCompare.compare(org.gjt.sp.jedit.pluginmgr.InstallPanel.Entry,org.gjt.sp.jedit.pluginmgr.InstallPanel.Entry)',
               'org.gjt.sp.jedit.gui.FilePropertiesDialog.FilePropertiesDialog(org.gjt.sp.jedit.View,org.gjt.sp.jedit.browser.VFSBrowser,org.gjt.sp.jedit.io.VFSFile[])',
               'org.gjt.sp.jedit.bufferset.BufferSetManager.BufferSetClosed.BufferSetClosed(org.gjt.sp.jedit.bufferset.BufferSet)',
               'org.gjt.sp.jedit.bufferset.BufferSetManager.BufferSetClosed.BufferSetClosed(org.gjt.sp.jedit.bufferset.BufferSet)',
               'org.gjt.sp.jedit.bufferset.BufferSet.BufferSet()',
               'org.gjt.sp.jedit.bufferset.BufferSet.handleMessage()',
               'org.gjt.sp.jedit.bufferset.BufferSet.handleMessage()',
               'org.gjt.sp.jedit.search.HyperSearchResults.HighlightingTree.appendString2html(java.lang.StringBuilder,java.lang.String)',
               'org.gjt.sp.jedit.textarea.Gutter.setSelectionAreaEnabled(boolean)',
               'org.gjt.sp.jedit.PluginJAR.load(java.lang.String,boolean)',
               'org.gjt.sp.jedit.TextUtilities.join(java.util.Collection<java.lang.String>,java.lang.String)',
               'org.gjt.sp.jedit.textarea.Anchor.preContentRemoved(int,int,int)',
               'org.gjt.sp.jedit.GUIUtilities.SizeSaver.SizeSaver(java.awt.Frame,java.awt.Container,java.lang.String)',
               'org.gjt.sp.jedit.jEdit.finishStartup(boolean,boolean,boolean,java.lang.String,java.lang.String[])'
               ]
    assert len(deprecated) == len(updated)
    if delete.count(oldmethod) > 0: return ''
    if deprecated.count(oldmethod) >0:
        ind = deprecated.index(oldmethod)
        return updated[ind]
    return oldmethod





# 创建不同方法的调用距离表
def createdistanInvocate():
    ds = Dataset()
    methods = ds.getAllInvocateMethod()
    matrix = infiniteMatrix((len(methods), len(methods)) )
    r = []
    for method in methods:
        r.append(method[0])
    print("Create matrix")

    invocations = ds.getAllMethodInvocation()
    count1 = count2 =0
    for invocation in  invocations:
        indexCallMethod = r.index(invocation.callMethod)
        try:
            indexCalledMethod = r.index(invocation.calledMethod)
            matrix[indexCallMethod][indexCalledMethod] = 1
            count1 +=1
        except ValueError:
            count2 +=1
    print("count1: %d, count2: %d, sum: %d" % (count1, count2, count2+count1))
    #index = r.index("com.microstar.xml.HandlerBase.resolveEntity(java.lang.String,java.lang.String)")
    #print( index ) #输入方法名可得其编号
    #print(r[index]) #输入编号可得方法名
    print("Foldy")
    matrix = folyd(matrix)
    print("Insert datatable")
    content = []
    sql = "insert into simDistance( callMethodName, calledMethodName, length) values (?, ?, ?)"
    for i in range(0, matrix.shape[0]):
        callMethod = r[i]
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] < Infinite :
                calledMethod = r[j]
                value = matrix[i][j]
                content.append((callMethod, calledMethod, value))
    ds.executemany(sql, content)
    ds.commit()
    print(len(content))





def spliteParams(oriname):        #处理比对数据Y
    index = oriname.find("(")
    right = oriname[index+1: ]
    resY = re.split('[,<]',right)
    return resY

def transferSql(oriname):            #处理比对方法参数Y,插入%以便查找数据库
    index = oriname.find("(")
    left = oriname[0:index+1]
    right = oriname[index+1: ]
    content = ""
    for item in re.split('[,<]', right):
        content = content  + item + "%"
    return left + "%" + content + "'"

#将goldSets中的方法转换成能够与数据库中的匹配方法，如补充参数的完整类型名等，其中，会出现有些goldset中的方法在系统中不存在，坑爹的鬼
def createBenchmark():
    path = "resource/benchmark/GoldSets/"
    ds = Dataset()
    setResult = {}
    ds.execute("delete from goldSets ")
    ds.commit()
    for file in os.listdir(path):
        with open(path + file, encoding='utf-8') as f:
            origiMethods = ""
            updatedMethods = ""
            for line in f:
                if line.find("\n") > 0 :
                    line = line[0:-1]
                origiMethods = origiMethods  + line + "\n"
                line = processGoldensets(line)
                if len(line) ==0 : continue
                matchName = getMatchMethodName(ds, line, updatedMethods)
                updatedMethods = updatedMethods + matchName + "\n"
            id = re.findall('\d+',file)                         #取出ID号
            ID = "".join(id)                                    #将list转换为字符串
            sql = "insert into goldSets(ID,methods, origiMethods) values ('%s','%s', '%s')" % (ID, updatedMethods, origiMethods)
            ds.execute(sql)
            ds.commit()


def getMatchMethodName(ds, oldMethod, updatedMethods):
    resY = spliteParams(oldMethod)  # 获得对比方法中参数
    sql = "select name from methodinfo where name like '" + transferSql(oldMethod)
    sqlresult = ds.execute(sql)
    methods = sqlresult.fetchall()  # 获得原方法中参数，以便后续对比
    for i in range(0, len(methods)):
        resX = spliteParams(methods[i][0])
        result = 1
        if (len(resX) != len(resY)):  # 如果两个数据长度不同，即参数个数不等，直接结果错误
            continue
        for j in range(0, len(resX)):
            if (resX[j].find(resY[j]) == -1):  # 参数匹配则设为1
                result = 0
        if result == 1:  # 比对完全正确则插入数据库
            return   methods[i][0]
    print(oldMethod)
    return ''


#createBenchmark()
def createEntrancePoint():
    ds = Dataset()
    goldsets = ds.getGoldSets()
    content = []
    sql = "delete from entrancePointInfo"
    ds.execute(sql)
    ds.commit()
    sql = "insert into entrancePointInfo( ID, methods) values (?, ?)"
    for goldset in goldsets:
        ID, methods = goldset.ID, goldset.methods
        methods = methods[: -1].split("\n")
        count = np.ceil( len(methods) /5 )
        slice = random.sample(methods, int(count))
        slice = "\n".join(slice)
        content.append((ID, slice))
    ds.executemany(sql, content)
    ds.commit()

#createEntrancePoint()
# 调用关系字典，key为(调用者，被调用者), value = 1
#invocationDic = {}
# 直接调用关系字典， key为调用者, value 为所有被key调用的方法

def recuitInvocate(invocationDic,invocatorDic, invocator, invocated, length):
    print("count: %d, lenght: %d" % (len(invocationDic.keys()), length))
    if length >= 11: return
    if (invocator, invocated) in invocationDic.keys():
        if invocationDic[invocator, invocated] > length:
            invocationDic[invocator, invocated] = length
    else:
        invocationDic[invocator, invocated] = length
    length +=1
    if invocated in invocatorDic.keys():
        for nextInvocated in invocatorDic[invocated]:
            recuitInvocate(invocationDic,invocatorDic,invocator, nextInvocated, length)


def createRecuitdistanInvocate():
    ds = Dataset()
    ds.execute("delete from simDistance")
    ds.commit()
    allInvocations = ds.getAllMethodInvocation()
    invocationDic ={}
    for invocation in allInvocations:
        invocationDic[invocation.callMethod, invocation.calledMethod] = 1
    ds.execute("select distinct(callmethodname) from methodinvocationinfo ")
    temp = ds.cursor.fetchall()
    invocators = []
    for item in temp:
        invocators.append(item[0])
    invocatorDic ={}
    #保存存在直接调用关系的方法对
    for invocator in invocators:
        invocatorDic[invocator] = []
    ds.execute("select callMethodName, calledMethodName from methodinvocationinfo")
    for invocation in ds.cursor.fetchall():
        invocation = MethodInovation(invocation)
        if( invocatorDic[invocation.callMethod].count(invocation.calledMethod) ==0):
            invocatorDic[invocation.callMethod].append(invocation.calledMethod)
    for invocator in invocators:
        for invocated in invocatorDic[invocator]:
            recuitInvocate(invocationDic, invocatorDic,invocator, invocated, 1)
    content = []
    sql = "insert into simDistance( callMethodName, calledMethodName, length) values (?, ?, ?)"
    for key in invocationDic.keys():
        content.append((key[0], key[1], invocationDic[key]))
    ds.executemany(sql, content)
    ds.commit()
createRecuitdistanInvocate()
#createEntrancePoint()


