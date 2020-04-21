#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 3/17/2020 10:45 AM
# @Author : QH
# @Site : WUXI
# @File : PICTURE.py
# @Software: PyCharm


#开始处理超站气象五参数据
def meteprocess(chaomete):
    chaomete['时间'] = chaomete['时间'].apply(lambda x: x.replace(second = 0))
    chaomete['时间'] = chaomete['时间'].apply(lambda x: x.replace(minute = 0))
    chaomete = chaomete.set_index('时间')
    for i in np.arange(len(chaomete.columns)):
        chaomete.iloc[:,i] = pd.to_numeric(chaomete.iloc[:,i], errors='coerce')

    chaomete.to_excel('处理后结果\\chaomete.xls')
    return chaomete

#开始处理超站常规六参数据
def normalprocess(chaonormal):
    chaonormal['时间'] = chaonormal['时间'].apply(lambda x: x.replace(second = 0))
    chaonormal['时间'] = chaonormal['时间'].apply(lambda x: x.replace(minute=0))
    chaonormal= chaonormal.set_index('时间')
    for i in np.arange(len(chaonormal.columns)):
        chaonormal.iloc[:,i] = pd.to_numeric(chaonormal.iloc[:,i], errors='coerce')
    chaonormal.iloc[:, 3:] = chaonormal.iloc[:,3:]*273/298

    chaonormal.to_excel('处理后结果\\chaonormal.xls')
    return chaonormal

#开始处理超站氮氧化物数据
def noxprocess(chaonox):
    chaonox['时间'] = chaonox['时间'].apply(lambda x: x.replace(second = 0))
    chaonox['时间'] = chaonox['时间'].apply(lambda x: x.replace(minute = 0))

    chaonox= chaonox.set_index('时间')
    for i in np.arange(len(chaonox.columns)):
        chaonox.iloc[:,i] = pd.to_numeric(chaonox.iloc[:,i], errors='coerce')
    chaonox = chaonox * 273 / 298


    chaonox.to_excel('处理后结果\\chaonox.xls')
    return chaonox

#开始处理超站辐射数据
def radiationprocess(chaoradiation):
    chaoradiation['时间'] = chaoradiation['时间'].apply(lambda x: x.replace(second = 0))
    chaoradiation['时间'] = chaoradiation['时间'].apply(lambda x: x.replace(minute = 0))
    chaoradiation= chaoradiation.set_index('时间')
    for i in np.arange(len(chaoradiation.columns)):
        chaoradiation.iloc[:,i] = pd.to_numeric(chaoradiation.iloc[:,i], errors='coerce')

    chaoradiation.to_excel('处理后结果\\chaoradiation.xls')
    return chaoradiation

#开始处理超站VOCs数据
def vocsprocess(chaovocs):

    chaovocs['时间'] = chaovocs['时间'].apply(lambda x: x.replace(second = 0))
    chaovocs['时间'] = chaovocs['时间'].apply(lambda x: x.replace(minute = 0))
    chaovocs= chaovocs.set_index('时间')
    for i in np.arange(len(chaovocs.columns)):
        chaovocs.iloc[:,i] = pd.to_numeric(chaovocs.iloc[:,i], errors='coerce')
    chaovoc2 = pd.DataFrame(chaovocs.iloc[:,0],index = chaovocs.index)


    chaovoc2.to_excel('处理后结果\\chaovocs.xls')
    return chaovoc2


#开始处理六站数据
def sixprocess(sixstation):
    sixstation.drop(index = 0,inplace = True)
    sixstation3 = sixstation.copy()
    sixstation3['时间'] = sixstation3['时间'].apply(lambda x: x.replace(second=0))
    sixstation3['时间'] = sixstation3['时间'].apply(lambda x: x.replace(minute=0))
    sixstation3.set_index('时间', inplace=True)
    sixstation3.sort_index(inplace=True)
    sixstation4 = sixstation3.iloc[:, 5:]
    sixstation5 = sixstation4.copy()
    for i in np.arange(len(sixstation5.columns)):
        sixstation5.iloc[:, i] = pd.to_numeric(sixstation5.iloc[:, i], errors='coerce')
    sixstation6 = sixstation3.iloc[:, :5]
    sixstation7 = pd.concat([sixstation6, sixstation5], axis=1)

    sixstation7.to_excel('处理后结果\\sixstation.xls')
    return sixstation7

def cityprocess():
    # 开始导入合并8市常规数据
    print('开始导入8市相关数据')
    la = os.listdir(path_file2 + '\\其他各市')
    city_normal = pd.DataFrame(columns=['初始化'])
    for i in np.arange(len(la), step=2):
        city_normal1 = pd.read_excel((path_file2 + '\\其他各市\\' + la[i + 1]), skiprows=1)
        city_normal2 = city_normal1.iloc[:, [0, 2, 9, 10, 11]]
        city_normal = pd.concat([city_normal, city_normal2], axis=1, join='outer')
    city_normal.drop('初始化', axis=1, inplace=True)


    # 开始导入合并8市常规数据
    city_mete = pd.DataFrame(columns=['初始化'])
    for i in np.arange(len(la), step=2):
        city_mete1 = pd.read_excel((path_file2 + '\\其他各市\\' + la[i]), skiprows=1)
        city_mete2 = city_mete1.iloc[:, [0, 1, 3, 4, 5, 7]]
        city_mete = pd.concat([city_mete, city_mete2], axis=1, join='outer')
    city_mete.drop('初始化', axis=1, inplace=True)


    city_normal.to_excel('处理后结果\\city_normal.xls')
    city_mete.to_excel('处理后结果\\city_mete.xls')
    return city_normal,city_mete





#开始绘制超站常规六参数图
def normalpicture(normalpara):
    chaonormal = normalpara.copy()
    chaonormal.reset_index(inplace=True)
    chaonormal.insert(loc = 1,column = '日期',value = chaonormal['时间'].apply(lambda x: str(x).split()[0]))
    chaonormal.drop(['时间'],axis = 1,inplace = True)
    normalmax = chaonormal.groupby(by = '日期').max()
    normalmin = chaonormal.groupby(by = '日期').min()
    normalmean = chaonormal.groupby(by = '日期').mean()

    x = normalmin.reset_index()
    x = x['日期'].apply(lambda x: str(x).split('-')[-1] + '日')

    #绘制常规六参最大值最小值浓度图
    a = ['PM1','PM2.5','PM10','SO2','O3','CO','NO2']
    for i in np.arange(6):
        fig = plt.figure(figsize=(16, 8), dpi=100)
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
        normalpm2 = fig.add_subplot(1, 1, 1)
        normalpm2.plot(x,normalmax.iloc[:,i+1],'r',label='%s最大值' % a[i+1])
        normalpm2.plot(x,normalmin.iloc[:,i+1],'g',label='%s最小值' % a[i+1])
        normalpm2.plot(x,normalmean.iloc[:,i+1],'y',label='%s平均值' % a[i+1])
        normalpm2.set_xticklabels(x,rotation = 45)
        normalpm2.set_xlim(x[0],x[-1:])
        normalpm2.set_ylabel('%s浓度(μg/m3)'% a[i+1])
        normalpm2.legend(loc = 'upper right', ncol = 5)
        fig.savefig('处理后结果\\%s图.png'% a[i+1])
        plt.close()

#开始绘制臭氧图
    grouped = chaonormal.groupby('日期')
    normalmax = chaonormal.groupby(by='日期').max().iloc[:,4]
    normalmin = chaonormal.groupby(by='日期').min().iloc[:,4]
    y = []
    for m in chaonormal['日期'].unique():
        a = []
        for i in np.arange(16):
            b = grouped.get_group(m).iloc[0 + i:7 + i, 5].mean()
            a.append(b)
        y.append(max(a))
    fig = plt.figure(figsize=(16, 8), dpi=100)
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
    normalpm2 = fig.add_subplot(1, 1, 1)
    normalpm2.plot(x, normalmax, 'r', label='O3最大值'  )
    normalpm2.plot(x, normalmin, 'g', label='O3最小值' )
    normalpm2.plot(x,y, 'y', label='O3-8H')
    normalpm2.set_xticklabels(x, rotation=45)
    normalpm2.set_xlim('01日', '31日')
    normalpm2.set_ylabel('O3浓度(μg/m3)')
    normalpm2.legend(loc='upper right', ncol = 5)

    fig.savefig('处理后结果\\O3-8H图.png' )
    plt.close()




#开始绘制气象参数日均值序列图
def metepicture(metepara):
    #开始绘制气象参数日均值序列图
    chaomete = metepara.copy()
    chaomete.reset_index(inplace = True)
    chaomete.insert(loc = 1,column = '日期',value = chaomete['时间'].apply(lambda x: str(x).split()[0]))
    chaomete.drop('时间',axis = 1, inplace = True)
    grouped2 = chaomete.groupby('日期').mean()
    grouped2.reset_index(inplace=True)
    x = grouped2['日期']
    x = x.apply(lambda x: str(x).split('-')[-1] )

    fig = plt.figure(figsize = (16,8),dpi =80)
    plt.subplots_adjust(right = 0.8)
    ax2 = fig.add_subplot(111)
    leg1 = ax2.bar(x,grouped2.iloc[:,3],alpha = 0.5,label = '气压', width = 0.6)
    ax2.set_xlim(int(x[0])-2,int(x[-1:]))
    ax2.set_ylim(100,104)
    ax2.set_xlabel('日 期')
    ax2.set_ylabel('气 压 (kPa)')
    ax3 = ax2.twinx()
    leg2 = ax3.plot(x,grouped2.iloc[:,1],'r',label = '温度', linewidth = 2)
    leg3 = ax3.plot(x,grouped2.iloc[:,2],'g',label = '湿度', linewidth = 2)
    ax3.set_ylabel('温 度（℃）、湿 度（%）')

    ax4 = ax2.twinx()
    rspine = ax4.spines['right']
    rspine.set_position(('axes', 1.1))
    leg4 = ax4.plot(x,grouped2.iloc[:,4],linestyle = '--',color = 'orange',label = '风速', linewidth = 2)
    ax4.set_ylabel('风 速（m/s）')

    legz = leg2+leg3+leg4
    labs = [l.get_label() for l in legz]
    legz.append(leg1)
    labs.append(leg1.get_label())
    ax4.legend(legz, labs, loc=0,fontsize = 15, ncol = 5)
    fig.savefig('处理后结果\\气象参数图')
    plt.close()

#开始绘制超站辐射数据图
def radiationpicture(radiationpara):
    chaoradiation = radiationpara.copy()
    chaoradiation.reset_index(inplace = True)
    chaoradiation.insert(loc = 1,column = '日期',value = chaoradiation['时间'].apply(lambda x: str(x).split()[0]))
    chaoradiation.drop('时间',axis = 1, inplace = True)
    grouped2 = chaoradiation.groupby('日期').mean()
    grouped2.reset_index(inplace=True)
    x = grouped2['日期']
    x = x.apply(lambda x: str(x).split('-')[-1] )
    fig = plt.figure(figsize = (16,8),dpi =80)
    ax = fig.add_subplot(111)
    leg1 = ax.plot(x,grouped2.iloc[:,1],'b',label = 'UV-A(W/m2)')
    ax.set_ylabel('UV-A(W/m2)')


    grouped2.iloc[:, 1].to_excel('处理后结果\\UV-A.xls')

    ax2 = ax.twinx()
    leg2 = ax2.plot(x,grouped2.iloc[:,2],'y',label ='UV-B(W/m2)')

    grouped2.iloc[:,2].to_excel('处理后结果\\UV-B.xls')#导出绘图数据

    ax2.set_ylabel('UV-B(W/m2)')


    ax.set_xlabel('日 期')
    ax.set_xlim(int(x[0])-1,int(x[-1:])-1)
    legz = leg1+leg2
    labs = [l.get_label() for l in legz]
    ax.legend(legz, labs, loc=0,fontsize = 15)
    fig.savefig('处理后结果\\辐射日均图')
    plt.close()


#臭氧时间变化图
def o3picture(sixstationpara1,chaonormalpara2):
    #臭氧时间变化图
    sixstation = sixstationpara1.copy()
    sixstation.reset_index(inplace=True)
    sixstation4 = sixstation.iloc[:,[0,2,16]]
    grouped = sixstation4.groupby('点位')
    fig = plt.figure(figsize=(16,8),dpi = 80)
    ax = fig.add_subplot(111)

    ls = 0
    for i in sixstation['点位'].unique():
        ls = grouped.get_group(i).sort_values('时间')
        ls.iloc[:, 2] = pd.to_numeric(ls.iloc[:, 2], errors='coerce')
        ls.drop('点位', inplace=True, axis=1)
        ax.plot(ls.iloc[:,0], ls.iloc[:,1],label = i)

    chaoo3 = chaonormalpara2.copy()
    ax.plot(chaoo3.index,chaoo3.iloc[:,4],label = '超站',color = 'c')
    ax.set_ylabel('O3浓度(μg/m3)')
    ax.set_xlabel('日 期(天）')
    ax.set_xlim(ls.iloc[0,0],ls.iloc[-1:,0])
    ax.legend(loc = 'upper center',ncol = 10)
    fig.savefig('处理后结果\\臭氧变化')
    plt.close()

#开始绘制氮氧化物图
def noxpicuture(noxpara,vocspara):
    #开始绘制氮氧化物图
    chaonox = noxpara.copy()
    chaovocs = vocspara.copy()
    chaonox.reset_index(inplace=True)
    chaovocs.reset_index(inplace=True)
    fig = plt.figure(figsize=(16,8),dpi = 80)
    ax = fig.add_subplot(111)
    ax.plot(chaonox.iloc[:,0],chaonox.iloc[:,1],label = "NO(42i)(μg/m3)")
    ax.plot(chaonox.iloc[:,0],chaonox.iloc[:,2],label ='NO2(42i)(μg/m3)')
    ax.plot(chaovocs.iloc[:,0],chaovocs.iloc[:,1],label =' VOCs(ppb)')
    plt.legend(ncol = 5)
    ax.set_xlabel('日期（天）')
    ax.set_ylabel('浓度')
    ax.set_xlim( chaonox.iloc[0, 0],  chaonox.iloc[-1:, 0])
    fig.savefig('处理后结果\\氮氧化物浓度变化图')
    plt.close()

#开始绘制臭氧与辐射关系图
def o3radiatonpicture(normalpara,radiationpara):
    #开始绘制臭氧与辐射关系图
    chaonormal = normalpara.copy()
    chaoradiation = radiationpara.copy()

    chaonormal.reset_index(inplace = True)
    chaoradiation.reset_index(inplace = True)
    fig = plt.figure(figsize=(16,8),dpi=80)
    ax = fig.add_subplot(111)
    leg1 = ax.plot(chaonormal.iloc[:,0],chaonormal.iloc[:,5],label= 'O3')


    leg2 = ax.plot(chaoradiation.iloc[:,0],chaoradiation.iloc[:,1],label= 'UV-A(W/m2)',color = 'r')
    leg3 = ax.plot(chaoradiation.iloc[:,0],chaoradiation.iloc[:,2],label= 'UV-B(W/m2)',color = 'g')


    ax.set_xlim(chaonormal.iloc[0, 0], chaonormal.iloc[-1:, 0])

    ax.set_xlabel('日 期（天）')

    # legz = leg1+leg2+leg3
    # labs = [l.get_label() for l in legz]

    plt.legend(ncol = 5)
    fig.savefig('处理后结果\\臭氧与辐射关系图.png')
    plt.close()

#开始臭氧与气象条件关系图
def o3metepicture(normal,mete):
    chaonormal = normal.copy()
    chaomete = mete.copy()
    chaonormal.reset_index(inplace=True)
    chaomete.reset_index(inplace=True)
    fig = plt.figure(figsize=(16,8),dpi=80)
    ax = fig.add_subplot(111)
    ax.plot(chaonormal.iloc[:, 0], chaonormal.iloc[:, 5], 'orange', label='O3')
    ax.set_ylabel('臭氧浓度（μg/m3)')
    ax.set_xlabel('日 期（天）')
    ax.set_xlim(chaonormal.iloc[0, 0], chaonormal.iloc[-1:, 0])
    fig.savefig('处理后结果\\臭氧浓度.png')
    plt.close()


    fig1 = plt.figure(figsize=(16,8),dpi=80)
    ax1 = fig1.add_subplot(211)
    leg1 = ax1.plot(chaomete.iloc[:,0],chaomete.iloc[:,2],'g',label = '湿度')
    ax1.set_ylabel('湿 度（%）')
    ax1.set_xlim(chaomete.iloc[0, 0], chaomete.iloc[-1:, 0])

    ax2 = ax1.twinx()
    leg2 = ax2.plot(chaomete.iloc[:,0],chaomete.iloc[:,1],'r',label = '温度')
    ax2.set_ylabel('温 度（℃）')
    legz1 = leg1 + leg2
    labs1 = [l.get_label() for l in legz1]
    ax2.legend(legz1, labs1, ncol=5)

    ax3 = fig1.add_subplot(212)
    leg3 = ax3.plot(chaomete.iloc[:,0],chaomete.iloc[:,3],'c',label = '气压')
    ax3.set_ylabel('气压（kPa）')
    ax3.set_xlabel('日 期（天）')

    ax4 = ax3.twinx()
    leg4 = ax4.plot(chaomete.iloc[:,0],chaomete.iloc[:,4],'m',label = '风速')
    ax4.set_ylabel('风速（m/s）')


    legz2 = leg3+leg4
    labs2 = [l.get_label() for l in legz2]
    ax4.legend(legz2, labs2, ncol=5)
    ax4.set_xlim(chaomete.iloc[0, 0], chaomete.iloc[-1:, 0])

    fig1.savefig('处理后结果\\臭氧与气象关系.png')
    plt.close()


#开始绘制雷达附加图
def lidarpicture(radiation,mete,normal):
    #开始绘制雷达附加图
    i = 0
    while True:
        a = input('是否绘制雷达附加图，否请按0，是请按1')
        if a == '1':
            chaoradiation = radiation.copy()
            chaomete = mete.copy()
            chaonormal = normal.copy()

            chaoradiation.reset_index(inplace = True)
            chaomete.reset_index(inplace = True)
            chaonormal.reset_index(inplace = True)

            begin = input('请输入开始时间：如2020-01-11')
            end = input('请输入结束时间：如2020-01-17')

            try:
                x = (chaonormal.iloc[:,0] >= pd.to_datetime(begin)) & (pd.to_datetime(end) >= chaonormal.iloc[:,0])
                x1 = (chaoradiation.iloc[:, 0] >= pd.to_datetime(begin)) & (pd.to_datetime(end) >= chaoradiation.iloc[:, 0])
            except:
                print('\033[31m输入时间格式错误，请重新输开始')
                input('按<enter>键退出程序')
                sys.exit()

            fig = plt.figure(figsize=(16,8),dpi=120)
            ax = fig.add_subplot(111)

            leg1 = ax.bar(chaoradiation.iloc[:,0][x1],chaoradiation.iloc[:,1][x1],width = 0.032,label = 'UVA(W/m2)',alpha = 0.5)
            leg2 = ax.plot(chaonormal.iloc[:, 0][x], chaonormal.iloc[:, 1][x], 'r', label='O3')

            ax.set_ylabel('O3(μg/m3、UVA(W/m2)')
            ax.set_xlabel('日 期（天）')


            ax1 = ax.twinx()
            ax1.set_ylabel('风速（m/s)')
            leg3 = ax1.plot(chaomete.iloc[:,0][x],chaomete.iloc[:,4][x],'g',label = '风速')


            legz = leg2 +leg3
            legz.append(leg1)
            labs = [l.get_label() for l in legz]
            ax1.legend(legz, labs, ncol=5)

            i = i + 1
            fig.savefig('处理后结果\\雷达附加图%s.png' % i)
            plt.close()
        else:
            print('\033[31m输入错误，请重新输开始')
            sys.exit()


#开始绘制pm2.5与排名pm10图
def pmpicture(normal):
    #开始绘制pm2.5与排名pm10图
    chaonormal = normal.copy()
    chaonormal.reset_index(inplace=True)
    fig = plt.figure(figsize=(16, 8), dpi=80)
    ax = fig.add_subplot(111)
    ax.plot(chaonormal.iloc[:, 0], chaonormal.iloc[:, 2], 'g', label='PM2.5')
    ax.plot(chaonormal.iloc[:, 0], chaonormal.iloc[:, 3], label='PM10')
    ax.set_ylabel('浓 度(μg/m3)')
    ax.set_xlabel('日 期 (天)')
    ax.set_xlim(chaonormal.iloc[0, 0], chaonormal.iloc[-1:, 0])
    plt.legend(ncol =4)
    fig.savefig('处理后结果\\PM2.5与PM10图1.png')
    plt.close()

    chaonormal = normal.copy()
    chaonormal.reset_index(inplace = True)
    fig = plt.figure(figsize=(16,8), dpi = 80)
    ax = fig.add_subplot(111)
    leg1 = ax.plot(chaonormal.iloc[:,0],chaonormal.iloc[:,2],'g',label = 'PM2.5')
    leg2 = ax.plot(chaonormal.iloc[:,0],chaonormal.iloc[:,3],label = 'PM10')
    ax.set_ylabel('浓 度(μg/m3)')
    ax.set_xlabel('日 期 (天)')
    ax.set_xlim(chaonormal.iloc[0, 0], chaonormal.iloc[-1:, 0])


    ax1= ax.twinx()
    leg3 = ax1.plot(chaonormal.iloc[:,0],(chaonormal.iloc[:,2]/chaonormal.iloc[:,3]),'r',label = 'PM2.5/PM10')
    ax1.set_ylabel('PM2.5/PM10（%）')


    legz = leg1+leg2+leg3
    labs = [l.get_label() for l in legz]
    ax1.legend(legz, labs, ncol=5)
    fig.savefig('处理后结果\\PM2.5与PM10图2.png')
    plt.close()

#绘制各站PM2.5和PM10浓度图
def sixpm(six,normal):
    sixstation = six.copy()
    chaonormal = normal.copy()
    sixstation.reset_index(inplace  = True)
    chaonormal.reset_index(inplace = True)

    ci = 0
    while True:
        a = input('是够绘制各市PM2.5、PM10图：是请按1，否请按0')
        if a == '1':
             #绘制PM2.5浓度图
            begin = input('请输入开始时间：如2020-01-12')
            end = input('请输入结束时间：如2020-01-17')
            fig = plt.figure(figsize=(16,8),dpi=80)
            ax = fig.add_subplot(111)
            grouped = sixstation.groupby('点位')

            try:
                for i in (sixstation['点位'].unique()):
                    x = (grouped.get_group(i).iloc[:, 0] >= pd.to_datetime(begin)) & (pd.to_datetime(end) >= grouped.get_group(i).iloc[:, 0])
                    ax.plot(grouped.get_group(i).iloc[:,0][x],grouped.get_group(i).iloc[:,6][x],label = i)
            except:
                print('\033[31m输入时间格式错误，请重新开始')
                input('按<enter>键退出程序')
                sys.exit()

            x = (chaonormal.iloc[:, 0] >= pd.to_datetime(begin)) & (pd.to_datetime(end) >= chaonormal.iloc[:, 0])
            ax.plot(chaonormal.iloc[:, 0][x], chaonormal.iloc[:, 2][x], label='超站')

            ax.set_xlabel('日 期（天）')
            ax.set_ylabel('PM2.5浓度（μg/m3)')

            ax.legend(loc = 'upper center',ncol = 10)
            ax.set_xlim(pd.to_datetime(begin),pd.to_datetime(end))
            fig.savefig('处理后结果\\各站PM2.5图%s.png' % str(ci))
            plt.close()

            #开始绘制PM10图
            fig = plt.figure(figsize=(16, 8), dpi=80)
            ax = fig.add_subplot(111)
            grouped = sixstation.groupby('点位')

            for i in (sixstation['点位'].unique()):
                x = (grouped.get_group(i).iloc[:, 0] >= pd.to_datetime(begin)) & (
                            pd.to_datetime(end) >= grouped.get_group(i).iloc[:, 0])
                ax.plot(grouped.get_group(i).iloc[:, 0][x], grouped.get_group(i).iloc[:, 8][x], label=i)

            x = (chaonormal.iloc[:, 0] >= pd.to_datetime(begin)) & (pd.to_datetime(end) >= chaonormal.iloc[:, 0])
            ax.plot(chaonormal.iloc[:, 0][x], chaonormal.iloc[:, 3][x], label='超站')

            ax.set_xlabel('日 期（天）')
            ax.set_ylabel('PM10浓度（μg/m3)')


            ax.legend(loc = 'upper center',ncol=10)
            ax.set_xlim(pd.to_datetime(begin), pd.to_datetime(end))
            fig.savefig('处理后结果\\各站PM10图%s.png' % str(ci))
            plt.close()
        else:
            print('\033[31m输入错误，请重新开始')
            sys.exit()
        ci += 1


    #开始绘制八市AQI图

def cityaqi(citynormal):
    print('开始绘制8市AQI图')
    city_normal = citynormal.copy()
    fig = plt.figure(figsize=(16, 8), dpi=80)
    ax = fig.add_subplot(111)
    res = pd.DataFrame()
    for i in np.arange(len(city_normal.columns) / 5):
        city_normal.iloc[:, int(1 + i * 5)] = pd.to_datetime(city_normal.iloc[:, int(1 + i * 5)], errors='coerce')
        ax.plot(city_normal.iloc[:, int(1 + i * 5)], city_normal.iloc[:, int(2 + i * 5)],
                label=city_normal.iloc[:, int(0 + i * 5)].drop_duplicates().values[0],linewidth=3)

        res = pd.concat([res, city_normal.iloc[:, int(2 + i * 5)]], axis=0, join='outer', sort=True)

    emp = res.max().values
    a = 0
    if emp <= 50:
        a = 50
    elif emp > 50 and emp <= 100:
        a = 100
    elif emp > 100 and emp <= 150:
        a = 150
    elif emp > 150 and emp <= 200:
        a = 200
    elif emp > 200 and emp <= 300:
        a = 300
    elif emp > 300:
        a = 500

    ax.set_ylim(0, a)

    ax.legend(loc=9, ncol=8, fontsize=15, bbox_to_anchor=(0.5, 1.1), edgecolor='#FFFFFF')

    ax.set_xlim(city_normal.iloc[:, 1][0], city_normal.iloc[:, 1][-1:])
    ax.axhspan(0, 50, facecolor=np.array([0, 176, 80]) / 255, alpha=.7)  # 绿
    ax.axhspan(50, 100, facecolor=np.array([254, 255, 0]) / 255, alpha=.7)  # 黄色
    ax.axhspan(100, 150, facecolor=np.array([255, 192, 3]) / 255, alpha=.7)  # 橙色
    ax.axhspan(150, 200, facecolor=np.array([255, 0, 0]) / 255, alpha=.7)  # 红色
    ax.axhspan(200, 300, facecolor=np.array([102, 0, 102]) / 255, alpha=.7)  # 紫色
    ax.axhspan(300, 1000, facecolor=np.array([102, 0, 0]) / 255, alpha=.7)  # 褐红色

    fig.savefig('处理后结果\\各市AQI图.png')
    plt.close()

def citymete(mete):

    print('开始绘制8市气象参数图')
    plt.switch_backend('agg')
    city_mete = mete.copy()
    for m in np.arange(4):
        fig = plt.figure(figsize=(16, 8), dpi=80)
        ax = fig.add_subplot(111)
        sign = city_mete.columns[2:6]
        for i in np.arange(len(city_mete.columns) / 6):
            city_mete.iloc[:, int(1 + i * 6)] = pd.to_datetime(city_mete.iloc[:, int(1 + i * 6)], errors='coerce')

            ax.plot(city_mete.iloc[:, int(1 + i * 6)], city_mete.iloc[:, int(m + 2 + i * 6)],
                    label=city_mete.iloc[:, int(0 + i * 6)].drop_duplicates().values[0])

        ax.text(0, 1.05, sign[m], backgroundcolor='orange', verticalalignment="top", transform=ax.transAxes)
        ax.set_ylabel(sign[m])

        ax.set_xlim(city_mete.iloc[:,1].min(),city_mete.iloc[:,1].max())
        ax.legend(loc=9, ncol=8, fontsize=14, bbox_to_anchor=(0.5, 1.07), edgecolor='#FFFFFF')

        fig.savefig('处理后结果\各市气象参数%s.png' % (m))
        plt.close()

def citynormal(citynormalpara):
    def get_label(s):
        if s == '—':
            return '\n' * 2
        else:
            reg = re.compile(r'.*?\((.*?)\).*?')
            res = '\n' + '\n'.join(reg.findall(s))
            return res + '\n' * (2 - res.count('\n'))

    def _map(series, func):
        return series.apply(func)

    data = citynormalpara.copy()
    l = len(data.columns)
    citys = ['南平', '厦门', '宁德', '泉州', '漳州', '福州', '莆田', '龙岩']
    data.iloc[:, 1] = pd.to_datetime(data.iloc[:, 1])
    col = data.iloc[:, 1].dt.day.apply(lambda s: f'{s}日')
    dt = pd.DataFrame(data.iloc[:, 2:l:5].values.T, index=citys, columns=col)
    # -------------------------处理需要的自定义标签--------------------------#
    labels = pd.DataFrame(data.iloc[:, 3:l:5].values.T, columns=dt.columns, index=dt.index)
    labels = labels.apply(_map, args=(get_label,))
    labels = dt.astype(str) + labels
    # -------------------------开始绘图--------------------------#
    colors = ['#00E400', '#FEFF00', '#FE7E00', '#FC0201']
    # emp = dt.max().max()
    # a = 0
    # if emp <= 50:
    #     a = 100
    #     colors2 = colors[:3]
    # elif emp > 50 and emp <= 100:
    #     a = 150
    #     colors2 = colors[:3]
    # elif emp > 100 and emp <= 150:
    #     a = 200
    #     colors2 = colors[:4]
    # elif emp > 150 and emp <= 200:
    #     a = 300
    #     colors2 = colors[:5]
    # elif emp > 200 and emp <= 300:
    #     a = 500
    #     colors2 = colors[:6]
    # elif emp > 300:
    #     a = 500
    #     colors2 = colors

    cm = mpl.colors.ListedColormap(colors)


    #绘制第一张日历图
    fig = plt.figure(figsize=(10, 8), dpi=120)
    ax = sns.heatmap(dt.iloc[:, :10], annot=labels.iloc[:, :10], fmt='', vmin=0, vmax=200, cmap=cm,
                     linewidths=0.5, linecolor='gray', cbar_kws={'pad': 0.03}, square=True)
    plt.ylim(-0.5, len(dt))

    plt.savefig('处理后结果\各市日历图1.png')
    plt.close()

    #绘制第二张日历图
    fig = plt.figure(figsize=(10, 8), dpi=120)
    ax = sns.heatmap(dt.iloc[:, 10:20], annot=labels.iloc[:, 10:20], fmt='', vmin=0, vmax=200, cmap=cm,
                     linewidths=0.5, linecolor='gray', cbar_kws={'pad': 0.03}, square=True)
    plt.ylim(-0.5, len(dt))

    plt.savefig('处理后结果\各市日历图2.png')
    plt.close()

    #绘制第三张日历图
    fig = plt.figure(figsize=(10, 8), dpi=120)
    ax = sns.heatmap(dt.iloc[:, 20:], annot=labels.iloc[:, 20:], fmt='', vmin=0, vmax=200, cmap=cm,
                     linewidths=0.5, linecolor='gray', cbar_kws={'pad': 0.03}, square=True)
    plt.ylim(-0.5, len(dt))
    plt.savefig('处理后结果\各市日历图3.png')
    plt.close()







if __name__ == '__main__':

    print('开始加载处理模块')
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    import seaborn as sns
    import os
    import re
    import sys
    plt.switch_backend('agg')

    print('开始进行系统配置')
    path_file = os.path.abspath('main.py')
    path_file2 = os.path.dirname(path_file)
    os.chdir(path_file2)
    if not os.path.exists((str(path_file2) + str('\\处理后结果'))):
        os.makedirs((str(path_file2) + str('\\处理后结果')))


    '''设置允许中文绘图'''
    plt.rcParams.update({'font.size': 15})
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']



    #开始导入相关数据：
    print('开始导入超站相关数据')
    try:
        chaonormal = pd.read_excel(r'超站常规数据小时值.xls',skiprows=1,parse_dates=['时间'])
    except:
        print('超站常规数据文件名错误')
    try:
        chaomete = pd.read_excel(r'超站气象五参小时值.xls',skiprows=1,parse_dates=['时间'])
    except:
        print('超站气象五参文件名错误')
    try:
        chaonox = pd.read_excel(r'超站氮氧化物.xls',skiprows=1,parse_dates=['时间'])
    except:
        print('超站氮氧化物文件名错误')
    try:
        chaoradiation = pd.read_excel(r'超站辐射数据.xls',skiprows=1,parse_dates=['时间'])
    except:
        print('超站辐射文件名错误')
    try:
        chaovocs = pd.read_excel(r'超站VOCS.xls',skiprows=1,parse_dates=['时间'])
    except:
        print('超站VOCs文件名错误')
    try:
        sixstation = pd.read_excel(r'其他常规六参监测_小时数据.xlsx',parse_dates=['时间'])
    except:
        print('六站文件名错误')





    #开始收集处理后的数据：
    print('开始处理数据')
    try:
        chaomete2 = meteprocess(chaomete)
    except:
        print('超站气象数据格式错误')
    try:
        chaonormal2 = normalprocess(chaonormal)
    except:
        print('超站常规数据格式错误')
    try:
        chaonox2 = noxprocess(chaonox)
    except:
        print('超站氮氧化物数据格式错误')
    try:
        chaoradiation2 = radiationprocess(chaoradiation)
    except:
        print('超站辐射数据错误')
    try:
        chaovocs2 = vocsprocess(chaovocs)
    except:
        print('超站VOCs数据格式错误')
    try:
        sixstation2 = sixprocess(sixstation)
    except:
        print('六站数据格式错误')
    try:
        city_normal,city_mete = cityprocess()
    except:
        print('其他各市数据格式错误')



    #开始绘制各种图片
    print('开始绘制图形')
    try:
        normalpicture(chaonormal2)
    except:
        print('缺少超站常规数据')
    try:
        metepicture(chaomete2)
    except:
        print('缺少超站气象数据')
    try:
        radiationpicture(chaoradiation2)
    except:
        print('缺少超站辐射数据')
    try:
        o3picture(sixstation2, chaonormal2)
    except:
        print('缺少六站数据或者超站常规数据')
    try:
        noxpicuture(chaonox2, chaovocs2)
    except:
        print('缺少超站氮氧化物或者VOCs数据')
    try:
        o3radiatonpicture(chaonormal2, chaoradiation2)
    except:
        print('缺少超站常规或者辐射数据')
    try:
        o3metepicture(chaonormal2, chaomete2)
    except:
        print('缺少超站常规或者气象数据')
    try:
        pmpicture(chaonormal2)
    except:
        print('缺少超站常规数据')
    try:
        sixpm(sixstation2,chaonormal2)
    except:
        print('缺少六站数据或超站常规数据')
    try:
        cityaqi(city_normal)
    except:
        print('缺少各市常规数据')
    try:
        citymete(city_mete)
    except:
        print('缺少各市气象数据')
    try:
        citynormal(city_normal)
    except:
        print('缺少各市常规数据')
    try:
        lidarpicture(chaoradiation2, chaomete2, chaonormal2)
    except:
        print('缺少超站常规或者气象或者雷达数据')


























