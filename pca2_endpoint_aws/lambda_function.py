import numpy as np
import math,json
#import sklearn.preprocessing as skpp
from sklearn.cluster import KMeans

def parse_data(climate_data,columns):
    col_idx =set()
    for col in columns:
        idx= list(climate_data[0]).index(col)
        col_idx.add(idx)
        
    columns_index = tuple(col_idx)
    print(columns_index)
    sel = [2,3,5,6,11,12,13]

    climate_nums=climate_data[1:,sel].astype(float)##neeeeeed to changeeeeeeee thissssssss 
    print(climate_nums)
    m,n = climate_nums.shape # num of states x num of factors
    States=climate_data[1:,1]
    Factors=climate_data[0,sel]
    #%%
    # normalize data
    stdA = np.std(climate_nums,axis = 0) #standard deviations for each category
    mean_nums = np.mean(climate_nums,axis = 0)
    climate_nums2 = (climate_nums-mean_nums) @ np.diag(np.ones(stdA.shape[0])/stdA)
    xc = climate_nums2.T
    #%% Covariance Matrix
    C = np.dot(xc,xc.T)/m
    #Finding the eigenvectors and eigenvalues
    S, W = np.linalg.eigh(C)
    # Sorting in order of decreasing magnitude eigenvalue
    W = W[:, np.argsort(-S)]
    S = S[np.argsort(-S)]
    #%%first two principal directions
    w1=np.real(W[:,0])
    w2=np.real(W[:,1])
    #%%Project State data onto these two principal directions
    dim1 = np.dot(w1.T,xc)/math.sqrt(np.real(S[0]))
    dim2 = np.dot(w2.T,xc)/math.sqrt(np.real(S[1]))
    # k-means
    k=4 #number of clusters
    dim1_array=np.reshape(dim1,(m,1))
    dim2_array=np.reshape(dim2,(m,1))
    dim_c=np.concatenate((dim1_array,dim2_array),axis=1)
    kmeans = KMeans(n_clusters=k).fit(dim_c)
    c_idx = kmeans.labels_
    c_idx = [int(c) for c in c_idx]
    return list(zip(States, c_idx))
def lambda_handler(event, context):
    # TODO implement
    data = [['', 'State', 'Precipitation', 'Temperature', 'Unnamed: 3',
        'Precipitation', 'Temperature', 'level_0', 'index', 'state',
        'state_abbr', 'Storm Injuries', 'Storm Deaths',
        'Lung Cancer Deaths', 'Unnamed: 0', 'index_left', 'NO2 Mean',
        'NO2 1st Max Value', 'NO2 AQI', 'O3 Mean', 'O3 1st Max Value',
        'O3 AQI', 'SO2 Mean', 'SO2 1st Max Value', 'SO2 AQI', 'CO Mean',
        'CO 1st Max Value', 'CO AQI', 'average_AQI', 'index_right',
        'WEEK', 'REGION', 'Pneumonea/Flu Deaths', 'All Deaths',
        '<1 year (all cause deaths)', '1-24 years (all cause deaths)',
        '25-44 years', '45-64 years (all cause deaths)',
        '65+ years (all cause deaths)\n'],
['0', 'AK', '3941.182926829268', '329.0731707317073', '',
        '39.41182926829268', '32.90731707317073', '1', '1', 'alaska',
        'AK', '0', '0', '-199.8185185185185', '1.0', '22.0',
        '18.84822881595882', '32.86264781209782', '30.938085135135136',
        '0.030583971814671818', '0.03897383172458172',
        '33.966571943371946', '3.83074168918919', '6.027383391248393',
        '7.607898578030717', '0.563585567084942', '0.8416455842985842',
        '8.15343445957', '20.166497529026948', '', '', '', '', '', '',
        '', '', '', '\n'],
['1', 'ND', '1832.2032520325204', '413.9593495934959', '',
        '18.322032520325205', '41.39593495934959', '34', '34',
        'north dakota', 'ND', '3', '3', '-87.16981132075468', '32.0',
        '549.0', '13.305868851937602', '25.52923495236041',
        '24.1271525705832', '0.03110663133507668',
        '0.040265979801196616', '34.35908285401684',
        '1.8008647869078191', '2.9388317525999024', '3.3546339567389944',
        '0.3855364150528065', '0.5674184558056032', '5.3997542082628405',
        '16.810155897400467', '', '', '', '', '', '', '', '', '', '\n'],
['2', 'MN', '2901.5317919075146', '423.2485549132948', '',
        '29.015317919075144', '42.32485549132948', '23', '23',
        'minnesota', 'MN', '0', '3', '44.42413793103449', '24.0',
        '413.0', '17.50416097111147', '31.98952058103477',
        '30.255307556716176', '0.03472979151297531',
        '0.04459492426962627', '38.20188385833197', '2.731949940427614',
        '4.378823864860453', '4.999878750798655', '0.4862203872204993',
        '0.7420837447364124', '7.249193807780273', '20.17656599340677',
        '1132.0', '26.294021250762338', '4.0', '4.114855468961545',
        '55.125901556557494', '1.5621733343487827', '1.3858466333769188',
        '3.1663913113259063', '11.005050637707882',
        '38.00283213619048\n'],
['3', 'ME', '4518.368421052632', '425.4342105263158', '',
        '45.183684210526316', '42.54342105263158', '19', '19', 'maine',
        'ME', '0', '1', '61.79375', '20.0', '345.0', '9.58544169637874',
        '17.806872279371266', '16.619056547411418',
        '0.029753539027914677', '0.03736112543008474',
        '31.87769771792877', '1.8097254214996576', '3.2626476135772053',
        '3.9590658264509417', '0.3267559421783224', '0.4776372397343232',
        '4.814255318289235', '14.317518852520097', '', '', '', '', '',
        '', '', '', '', '\n'],
['4', 'VT', '4425.422222222222', '432.2', '',
        '44.254222222222225', '43.22', '45', '45', 'vermont', 'VT', '0',
        '2', '52.0', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '\n'],
['5', 'WY', '1331.4315068493152', '433.94520547945206', '',
        '13.314315068493151', '43.394520547945206', '50', '50',
        'wyoming', 'WY', '1', '3', '48.22608695652175', '46.0', '787.0',
        '9.979473734364351', '18.827968313433047', '17.84153654778019',
        '0.040001571520185714', '0.04770941180224295',
        '40.935210972555744', '1.9267772058083072', '2.904204251591514',
        '3.2619250283887267', '0.3211992801700527', '0.4837180396359857',
        '4.578505539908585', '16.65429452215831', '', '', '', '', '', '',
        '', '', '', '\n'],
['6', 'MT', '1531.3713080168777', '437.52742616033754', '',
        '15.313713080168776', '43.75274261603376', '26', '26', 'montana',
        'MT', '10', '2', '-112.21607142857144', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '\n'],
['7', 'NH', '4639.708333333333', '442.4375', '',
        '46.39708333333333', '44.24375', '29', '29', 'new hampshire',
        'NH', '0', '0', '54.84', '27.0', '464.0', '9.25836262421411',
        '19.25438348499544', '18.084491752930013',
        '0.027929009623702945', '0.03944558459248188',
        '33.68763128679011', '1.3667057686056756', '3.399384927608507',
        '4.384257595193504', '0.379735095545116', '0.5470110664137295',
        '5.421744428535749', '15.394531265862346', '', '', '', '', '',
        '', '', '', '', '\n'],
['8', 'WI', '3319.5105263157893', '443.37894736842105', '',
        '33.19510526315789', '44.3378947368421', '49', '49', 'wisconsin',
        'WI', '56', '9', '48.9638888888889', '45.0', '770.0',
        '17.464119416606298', '30.130216762914664', '28.43210908651255',
        '0.025148998357300133', '0.03317197024491493',
        '28.381163618020377', '2.692394630610549', '3.864834030298487',
        '5.3886366261888305', '0.4239188258529975', '0.5994089119991146',
        '6.137904783913918', '17.084953528658914', '2116.0',
        '26.293827440886265', '3.0', '7.780801484939745',
        '105.4997219022112', '2.3391315538929303', '1.6911348795762942',
        '6.367435613392487', '23.033262561247344', '71.93861541312786\n'],
['9', 'MI', '3327.0378378378377', '455.2648648648649', '',
        '33.270378378378375', '45.52648648648649', '22', '22',
        'michigan', 'MI', '5', '3', '57.84216867469879', '23.0', '396.0',
        '11.966150175109167', '24.020979969670442', '22.60807706310111',
        '0.02337311920090515', '0.03233616944946198',
        '27.716724514878834', '1.4632554186964275', '4.1241379507928775',
        '5.652388876223222', '0.2720750792461862', '0.4668312592818256',
        '4.964745060791102', '15.23548387874857', '1077.0',
        '26.406509987507555', '3.0', '6.546130257378894',
        '93.73485743637572', '2.8012272644230487', '2.685913906219302',
        '7.481895656754621', '24.163466774935603',
        '56.584708483744116\n'],
['10', 'SD', '2113.9805194805194', '457.47402597402595', '',
        '21.139805194805195', '45.7474025974026', '41', '41',
        'south dakota', 'SD', '14', '6', '-57.72878787878784', '39.0',
        '668.0', '16.962949697400738', '30.039464037243004',
        '28.23075424802793', '0.03599763033751451',
        '0.044932507306349394', '38.48763605327815',
        '2.5436205308418463', '4.005934796327427', '4.5986301298897665',
        '0.4803229749127116', '0.7254333526445096', '6.8936389418737845',
        '19.552664843267408', '', '', '', '', '', '', '', '', '', '\n'],
['11', 'ID', '1739.2357142857143', '457.48571428571427', '',
        '17.392357142857144', '45.748571428571424', '12', '12', 'idaho',
        'ID', '5', '1', '-61.32045454545453', '13.0', '226.0',
        '14.987883129496405', '31.61581678657075', '29.90897617905675',
        '0.0369995857713829', '0.05016548201438848',
        '43.125374260591535', '2.035201123101519', '3.5436472901678653',
        '4.052644596652666', '0.3882065987210232', '0.6036032549960034',
        '5.9748020268706705', '20.7654492657929', '667.0',
        '26.015288544358317', '8.0', '3.5199172364047313',
        '47.985170402623226', '1.2166190686923466', '1.1557425721532786',
        '2.5008910165777207', '8.663329026701119', '34.44386798703384\n'],
['12', 'CO', '1637.2241379310344', '460.375', '',
        '16.372241379310346', '46.0375', '5', '5', 'colorado', 'CO', '7',
        '16', '-139.52187499999994', '5.0', '90.0', '16.848888213581052',
        '36.925242233677274', '34.88001050686851', '0.02326272210865915',
        '0.03891184866812563', '33.36251281294771', '1.0262107598370738',
        '3.9193554839426965', '5.307258778991861', '0.41532762471686985',
        '0.7313683371689558', '6.873226802385196', '20.10575222529832',
        '263.0', '26.20235394285428', '8.0', '4.183967848613772',
        '64.54347462060636', '1.892798869710539', '1.7725249680733368',
        '4.655130397661367', '13.831315811204373', '42.35226231259567\n'],
['13', 'NY', '4265.261146496815', '472.2929936305732', '',
        '42.652611464968146', '47.22929936305732', '32', '32',
        'new york', 'NY', '14', '5', '56.71129032258063', '30.0',
        '515.0', '15.275891011589735', '29.05556863716716',
        '27.412321999864755', '0.025554888356722025',
        '0.03690608722514298', '31.51156658309233', '2.6981239133714663',
        '5.1015506862241695', '6.717331687551567', '0.30272540718734875',
        '0.4616498881730151', '4.532174973110833', '17.543348810904874',
        '1511.0', '26.35511706251892', '2.0', '11.086613889750948',
        '201.5713687951014', '2.789314827373788', '3.2286112899294435',
        '11.878602336779855', '41.114424937932135',
        '142.39266942124826\n'],
['14', 'IA', '3517.958620689655', '481.8137931034483', '',
        '35.17958620689655', '48.18137931034483', '15', '15', 'iowa',
        'IA', '20', '5', '48.324242424242414', '16.0', '277.0',
        '12.818245193242054', '23.911142873664627', '22.337065947957658',
        '0.026749044846064947', '0.03585730891040742',
        '30.616180020201238', '1.5080021044906953', '2.7123681326344595',
        '3.1093717056478067', '0.3640577828983116', '0.5591704349792233',
        '5.313761921167559', '15.344094898743565', '647.0',
        '26.055168205214454', '4.0', '6.998090066561388',
        '73.53412948000367', '1.2030809847807995', '1.1922692651508564',
        '3.2548888754716687', '14.122903221594248',
        '53.72872192776217\n'],
['15', 'MA', '4853.5', '485.29411764705884', '', '48.535',
        '48.529411764705884', '21', '21', 'massachusetts', 'MA', '1',
        '0', '55.45', '22.0', '379.0', '18.3463045973538',
        '31.35594317129859', '29.721822766065802', '0.02112799205318273',
        '0.030625376367675136', '26.01334107058591',
        '2.4112521792536947', '4.673959382057287', '5.793637356328532',
        '0.28756122068204104', '0.4838062884039962', '4.738155312484193',
        '16.566739126366105', '967.0', '25.82798327909489', '1.0',
        '4.532573457122119', '45.251874166265154', '1.0069747820004546',
        '0.951113520563604', '2.744737967200808', '9.32721662096884',
        '31.179330924419556\n'],
['16', 'UT', '1425.5670731707316', '491.5060975609756', '',
        '14.255670731707317', '49.15060975609756', '44', '44', 'utah',
        'UT', '0', '2', '-168.78620689655173', '42.0', '719.0',
        '21.462723104674026', '37.48820931780365', '35.43397582816519',
        '0.03497296880955983', '0.046282225533202166',
        '39.68367920133111', '2.7467585244289823', '4.3287389593102406',
        '4.914727402968106', '0.5305730339585539', '0.8441781533807292',
        '8.041209903125862', '22.018398083897566', '1951.0',
        '26.279616758242305', '8.0', '6.362809951329044',
        '77.61754969819025', '2.2136350379446177', '2.4067281364605884',
        '5.503863408293348', '14.913482485490587', '52.54339925584129\n'],
['17', 'NE', '2464.3494623655915', '493.03225806451616', '',
        '24.643494623655915', '49.303225806451614', '27', '27',
        'nebraska', 'NE', '7', '5', '-141.3483870967742', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '\n'],
['18', 'CT', '4980.888888888889', '496.1111111111111', '',
        '49.80888888888889', '49.61111111111111', '6', '6',
        'connecticut', 'CT', '2', '3', '52.2375', '6.0', '107.0',
        '16.60398132406509', '32.02377990365427', '30.227869162540635',
        '0.029507898728847726', '0.04120318170684323',
        '35.16391634836561', '2.2764476938725684', '4.435530070497731',
        '4.726441971710481', '0.4834570980691253', '0.6877255491895574',
        '6.201998129228512', '19.080056402961308', '318.0',
        '25.960910057232674', '1.0', '4.0263031054413165',
        '37.28437010889258', '0.7405154210788552', '0.8117881351064449',
        '2.276779734923553', '7.499116269943702', '25.94166319316839\n'],
['19', 'PA', '4358.96644295302', '496.79194630872485', '',
        '43.5896644295302', '49.67919463087249', '38', '38',
        'pennsylvania', 'PA', '67', '6', '51.937313432835815', '36.0',
        '617.0', '11.597142608822008', '24.221324300692547',
        '22.829485589532318', '0.02452437552178449',
        '0.03922119085589169', '33.59977758449816', '2.3711230913494123',
        '5.069267764388844', '7.100379346317734', '0.22070417090423727',
        '0.37805612258724586', '3.5744575222284136',
        '16.776025010644158', '1731.0', '26.238270640701533', '2.0',
        '6.241485004584215', '104.22372521927014', '2.203306016304615',
        '2.452968519667675', '6.751242816965807', '22.999677171587066',
        '69.77465421014358\n'],
['20', 'WA', '3808.774834437086', '498.0927152317881', '',
        '38.08774834437086', '49.80927152317881', '47', '47',
        'washington', 'WA', '14', '1', '56.73076923076921', '44.0',
        '753.0', '20.457376448893573', '36.13725521601686',
        '34.012401264488936', '0.030955042360379336',
        '0.040465386722866176', '35.44042655426765',
        '3.0620411275026345', '5.0866455637513175', '5.894027291886194',
        '0.5143902687038988', '0.7822797766069546', '7.511756926589392',
        '20.714653009308048', '2061.0', '26.492425579107557', '9.0',
        '6.029718423951768', '94.95500253818369', '1.5164618719665783',
        '2.111477339363085', '5.394242389111282', '19.76686071447972',
        '66.06329858180041\n'],
['21', 'OR', '3598.3333333333335', '501.3802083333333', '',
        '35.983333333333334', '50.13802083333333', '37', '37', 'oregon',
        'OR', '0', '4', '55.44166666666667', '35.0', '600.0',
        '15.742389006284736', '27.377922651592232', '25.83625591915999',
        '0.02633397308449157', '0.03607110190651298',
        '30.788924220497165', '2.210933325472454', '3.353163395724547',
        '4.031287704604294', '0.4276911952239042', '0.7045544281648821',
        '6.915181752806926', '16.892912399267093', '1676.0',
        '26.64291370654542', '9.0', '8.047240843232252',
        '126.93760003508494', '2.332869811856928', '2.6158371329432466',
        '7.4721356852901515', '26.877803481081962',
        '87.54795549159974\n'],
['22', 'RI', '4914.909090909091', '504.8181818181818', '',
        '49.14909090909091', '50.481818181818184', '39', '39',
        'rhode island', 'RI', '0', '0', '53.44', '37.0', '634.0',
        '16.547107580766337', '28.72132817430504', '27.12757190082645',
        '0.03542596378662659', '0.04560492336589026',
        '39.20350653643877', '2.419674635612322', '4.0433196543951935',
        '5.005158127406751', '0.4791596656649135', '0.7249227738542453',
        '7.071647240503102', '19.601970951293765', '1786.0',
        '26.762775044185467', '1.0', '3.5997119094289456',
        '58.86989070957468', '1.4639036632378402', '1.1699286202231391',
        '2.7847003099880707', '11.061305677582476',
        '42.39005243854316\n'],
['23', 'OH', '3975.2301587301586', '512.1031746031746', '',
        '39.75230158730159', '51.210317460317455', '35', '35', 'ohio',
        'OH', '219', '11', '60.149999999999984', '33.0', '566.0',
        '13.845319806763287', '24.795349601168407', '23.315864419728122',
        '0.0331847479833726', '0.04316758993371539', '36.97958916975621',
        '2.7878788821480733', '5.156383188405796', '6.518581862252601',
        '0.4968388242894058', '0.7028848974272556', '6.901272938280173',
        '18.428827097504282', '1566.0', '26.289996722409477', '3.0',
        '7.460760210009056', '109.76957737460688', '2.3371704693659336',
        '2.0691085056869563', '5.914281110045351', '22.82273816960979',
        '76.60421542118749\n'],
['24', 'WV', '4546.85294117647', '518.0980392156863', '',
        '45.468529411764706', '51.80980392156863', '48', '48',
        'west virginia', 'WV', '3', '2', '70.62', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '\n'],
['25', 'NV', '916.675', '519.75', '', '9.16675', '51.975', '28',
        '28', 'nevada', 'NV', '4', '25', '-79.48823529411763', '26.0',
        '447.0', '9.212272400984089', '19.61157801908996',
        '18.535556163110737', '0.031535224541438575',
        '0.038934137729122416', '33.338814783527546',
        '0.1569286819340155', '0.5688869287048542', '0.7802295402013755',
        '0.0982602972937346', '0.23841006373326654', '3.058969641189352',
        '13.928392532007251', '1456.0', '26.49816664254354', '8.0',
        '16.627383156373234', '250.73054151407646', '3.2934844876405927',
        '5.79634922245463', '18.106990363284453', '59.8775417072716',
        '163.4849292618261\n'],
['26', 'IN', '4254.844036697248', '519.7981651376147', '',
        '42.54844036697248', '51.97981651376146', '14', '14', 'indiana',
        'IN', '8', '3', '64.28478260869565', '15.0', '260.0',
        '12.08009650521907', '27.070809356168123', '25.441628610871504',
        '0.027062166011590102', '0.04256945614883451',
        '36.435128385858505', '1.858936796838237', '3.990353843823247',
        '4.91530188691342', '0.37459833393175257', '0.5507809035110299',
        '5.1197473847092905', '17.977951567088176', '777.0',
        '26.268604722943195', '3.0', '4.841128154984559',
        '78.6945415601552', '1.895712585220377', '1.8921883295582398',
        '4.738024812159849', '16.68071835035656', '53.46808181003289\n'],
['27', 'IL', '4019.414201183432', '521.7041420118343', '',
        '40.194142011834316', '52.170414201183426', '13', '13',
        'illinois', 'IL', '15', '12', '59.8078431372549', '14.0',
        '243.0', '15.763726430543684', '30.175783103064962',
        '28.488879930833548', '0.020822758701425925',
        '0.03291531265166715', '28.113743929497822',
        '1.6972251446571691', '4.312491048683949', '5.9090527019717225',
        '0.3880666385239469', '0.5968882672149936', '5.779833115981378',
        '17.072877419571117', '722.0', '25.901403674393073', '3.0',
        '9.800505083112492', '138.3618577311463', '3.356332689731542',
        '3.7997158786766425', '11.135460979896068', '32.92738245007127',
        '86.8155273302736\n'],
['28', 'NJ', '4711.347826086957', '528.804347826087', '',
        '47.11347826086957', '52.8804347826087', '30', '30',
        'new jersey', 'NJ', '2', '0', '53.823809523809516', '28.0',
        '481.0', '16.14234022267841', '30.645909222763194',
        '28.937375120044432', '0.023864634998649083',
        '0.035957945188938696', '30.773045300852928',
        '2.310659217780579', '4.983858460078769', '5.902087902504285',
        '0.3925377010030792', '0.5814373624052876', '5.65213595289752',
        '17.8161610690748', '1352.0', '25.70997456939307', '2.0',
        '1.48014440860152', '30.520030403234326', '1.1074232240818211',
        '0.889936791751424', '3.0584647957899187', '7.750498337171309',
        '17.687735175579796\n'],
['29', 'NM', '1485.9891891891891', '540.5837837837838', '',
        '14.859891891891891', '54.05837837837838', '31', '31',
        'new mexico', 'NM', '12', '2', '39.56363636363636', '29.0',
        '498.0', '20.256976130221133', '36.381069997270004',
        '34.18797941577941', '0.036855106988806986',
        '0.04760801774501765', '40.924271253071254',
        '2.5317947058422066', '4.061215555555556', '4.753868045293512',
        '0.4874754565929567', '0.7856311700791703', '7.395238492041463',
        '21.815339301546413', '1407.0', '26.66078431372549', '8.0',
        '8.546921274557235', '122.44981552627502', '1.701499694862625',
        '3.0944872585383134', '9.542144182943296', '25.723137571106488',
        '82.34325437706126\n'],
['30', 'KS', '3070.0301204819275', '544.722891566265', '',
        '30.700301204819276', '54.4722891566265', '16', '16', 'kansas',
        'KS', '17', '1', '17.474285714285713', '17.0', '294.0',
        '9.304742698998304', '19.596788651771377', '18.52941952705997',
        '0.02613887540942068', '0.037488770631740026',
        '32.084366772188396', '1.8147883468248789', '3.455266251855694',
        '4.862791301995637', '0.2911443265781793', '0.4580609023093861',
        '4.89191459505447', '15.092123049074619', '832.0',
        '25.728504959488674', '4.0', '3.585919891096453',
        '57.12352000201932', '1.2293725819134271', '1.8365417474744443',
        '4.040314553147638', '12.837194585259619', '37.1277186164954\n'],
['31', 'MO', '4363.962025316456', '549.4493670886076', '',
        '43.63962025316456', '54.94493670886076', '25', '25', 'missouri',
        'MO', '107', '14', '62.76869565217391', '25.0', '430.0',
        '12.543772551268233', '27.29687897805016', '25.75614735991792',
        '0.02655914338567913', '0.04112153580820651',
        '35.306451290946825', '1.979111716156892', '5.396214203525795',
        '7.634280326287032', '0.42450419102855386', '0.6465994050943097',
        '6.580832590053892', '18.81942789180142', '1187.0',
        '26.595203910512105', '4.0', '6.949750865025194',
        '117.74982873176596', '4.1990431171397535', '4.538971724820675',
        '9.410958851238824', '29.176126221311367', '69.97163870411218\n'],
['32', 'MD', '4395.46', '551.1', '', '43.9546', '55.11', '20',
        '20', 'maryland', 'MD', '1', '4', '60.96250000000001', '21.0',
        '362.0', '14.804214230000104', '29.96522308056631',
        '28.30340549986381', '0.031246292777168238',
        '0.043738009691620124', '37.57475050929842',
        '2.7900842427944674', '5.688535023774367', '6.430188767134966',
        '0.44340082779331297', '0.6944711497081151', '6.342293267636662',
        '19.66265951098347', '1022.0', '26.61111111111111', '5.0',
        '15.720125786163518', '173.73685695855502', '3.4474278342202873',
        '5.687711659409772', '17.991936784389612', '47.41835994194485',
        '99.11929527495563\n'],
['33', 'DE', '4591.666666666667', '556.3333333333334', '',
        '45.91666666666667', '55.63333333333334', '7', '7', 'delaware',
        'DE', '4', '0', '64.2', '8.0', '141.0', '19.254366278656125',
        '33.585183399209484', '31.708958893280638',
        '0.03283761324110675', '0.04272762450592887',
        '36.655389723320155', '2.897398474308301', '4.725719288537549',
        '5.596619458620656', '0.505925473320158', '0.7741794703557313',
        '7.485922987146572', '20.361722765592006', '428.0',
        '24.954186118892004', '5.0', '1.5119540596973082',
        '16.97244537980757', '0.15976033804372688', '0.2652257000203726',
        '1.4759148211238484', '3.6169218136106784',
        '11.447500199886436\n'],
['34', 'VA', '4407.741379310345', '557.6034482758621', '',
        '44.07741379310345', '55.76034482758621', '46', '46', 'virginia',
        'VA', '18', '6', '62.91194029850743', '43.0', '736.0',
        '12.352821423221044', '24.71483693013688', '23.31261988650509',
        '0.024944412655896864', '0.03783870258936639',
        '32.46579743234489', '2.6355885981827747', '5.428442874009493',
        '6.283971898854463', '0.43053110464194105', '0.5806128350901865',
        '5.279765009219421', '16.835538556730963', '2006.0',
        '25.775579975579976', '5.0', '2.792735709948824',
        '56.244047952654505', '2.081719343194753', '1.9713496733988536',
        '4.333016239983453', '13.968690492870822', '33.83282124675568\n'],
['35', 'KY', '4824.2947368421055', '559.578947368421', '',
        '48.242947368421056', '55.95789473684211', '17', '17',
        'kentucky', 'KY', '4', '11', '80.79666666666667', '18.0',
        '311.0', '10.615583869880703', '23.53294021831256',
        '22.07452747281173', '0.027785478138961983',
        '0.039912933400156135', '34.343236432835056',
        '1.9273681430010705', '4.865340936351704', '7.236393132730992',
        '0.14422932697084592', '0.3301382453239732',
        '2.8479347355340128', '16.625522943477947', '857.0',
        '26.563289760348578', '6.0', '4.954317509404452',
        '66.60190859550829', '1.5671879900699728', '1.6125963990928844',
        '4.446472301762719', '15.638932487471148', '43.33458266497483\n'],
['36', 'TN', '5355.347826086957', '577.9347826086956', '',
        '53.55347826086957', '57.79347826086956', '42', '42',
        'tennessee', 'TN', '4', '6', '72.1663157894737', '40.0', '685.0',
        '10.809552488839683', '18.343887073694404', '17.165541228414703',
        '0.03700571688966566', '0.04390920933213757',
        '37.57215286647553', '2.368638885783924', '4.204187345722653',
        '4.659814599685193', '0.39567852321197133', '0.5726977768264319',
        '5.440933468869353', '16.209610540861195', '1841.0',
        '26.460762103462482', '6.0', '8.994184815032982',
        '124.4021712752996', '2.6595946323892425', '3.1487527164771847',
        '8.569000367456635', '29.094564122274083', '80.8950134506583\n'],
['37', 'NC', '5015.949367088608', '586.0443037974684', '',
        '50.15949367088608', '58.60443037974684', '33', '33',
        'north carolina', 'NC', '10', '17', '62.00200000000002', '31.0',
        '532.0', '10.616104301797321', '24.362754308834614',
        '22.979754726271075', '0.028138241529771704',
        '0.043731750386762316', '37.883554449094106',
        '1.376899657089834', '3.8659600765173434', '4.019641271266464',
        '0.3944143763623836', '0.5914163078725961', '5.702103237799041',
        '17.646263421107673', '1242.0', '26.453929539295398', '5.0',
        '10.049259364146618', '109.8536192038263', '2.9915080573156967',
        '2.920850688913275', '8.281440640966643', '24.243209199145692',
        '71.38192994048956\n'],
['38', 'CA', '2323.021220159151', '595.554376657825', '',
        '23.230212201591513', '59.55543766578249', '4', '4',
        'california', 'CA', '81', '31', '32.467241379310344', '4.0',
        '73.0', '10.855548719200597', '21.33056503549208',
        '20.132774246886246', '0.02719102579948019',
        '0.03827334915742909', '32.626921071272484',
        '1.1243524878111766', '2.2094955831365515', '3.0100416835185184',
        '0.35213966931962115', '0.5520341936777684',
        '5.6010540007416365', '15.34269775060472', '208.0',
        '26.371740051506663', '9.0', '11.641476467793346',
        '119.96771014894595', '2.075799113469292', '2.7894742990791217',
        '7.394826055428036', '24.414693416159967', '83.25871220981837\n'],
['39', 'OK', '3733.4656488549617', '597.8320610687023', '',
        '37.33465648854962', '59.783206106870225', '36', '36',
        'oklahoma', 'OK', '88', '12', '63.732467532467524', '34.0',
        '583.0', '6.817581780983961', '15.68422448739874',
        '14.763377972000644', '0.029871472445210268',
        '0.0427940295490809', '36.71404046035472', '0.552841191106783',
        '1.8928873978167249', '2.5213467796045537',
        '0.08528481105912669', '0.19205626508297186',
        '2.0967906167315022', '14.023888957172856', '1621.0',
        '26.560386473429947', '7.0', '7.750922011176317',
        '126.66269465654207', '1.9458607657951381', '2.606683354017234',
        '7.613963035415046', '26.94977493111209', '87.52880145558571\n'],
['40', 'AR', '5098.280373831775', '605.0', '',
        '50.982803738317756', '60.5', '3', '3', 'arkansas', 'AR', '20',
        '5', '71.68533333333335', '3.0', '56.0', '15.242760379698431',
        '29.139234886259988', '27.49768683863628', '0.02977347613986085',
        '0.041453919735968084', '35.46927734983643',
        '3.1681384179952947', '4.592985044310195', '5.3997045229102465',
        '0.5828264716946359', '0.8226105995328559', '7.926960650313356',
        '19.073407340424076', '98.0', '26.30994674482069', '7.0',
        '2.3763935988844818', '74.00459497839392', '2.3985427980988465',
        '2.5302202510066794', '5.09214105369171', '17.767411912647365',
        '46.097082566442005\n'],
['41', 'AZ', '1310.3699421965318', '623.1445086705203', '',
        '13.103699421965318', '62.31445086705203', '2', '2', 'arizona',
        'AZ', '17', '9', '42.58', '2.0', '39.0', '17.255992693109178',
        '36.55729922940005', '34.50439491754568', '0.02592607518520289',
        '0.043643478464216214', '37.42274095623954',
        '1.2542661699020916', '2.4909746220680047', '3.5505290063986656',
        '0.39680114806552297', '0.7448443362358907', '7.421470933731056',
        '20.724783953478735', '153.0', '26.98008022090725', '8.0',
        '9.538893938691283', '150.26858305963023', '3.515121976706648',
        '4.849557619936517', '11.175144072826974', '31.6175695063276',
        '97.32544200621473\n'],
['42', 'SC', '4877.919191919192', '625.3434343434343', '',
        '48.779191919191916', '62.53434343434343', '40', '40',
        'south carolina', 'SC', '23', '7', '62.84130434782611', '38.0',
        '651.0', '4.631170820700546', '9.312682866770183',
        '8.919165230779797', '0.032152866876289814',
        '0.042533264231889495', '36.574197624171184',
        '1.1145913897624349', '2.8356920812483315', '4.0410231996677615',
        '0.2352823788717041', '0.3252670682705209', '2.8661188761085623',
        '13.10012623268183', '', '', '', '', '', '', '', '', '', '\n'],
['43', 'AL', '5668.2', '627.978947368421', '',
        '56.681999999999995', '62.7978947368421', '0', '0', 'alabama',
        'AL', '104', '28', '62.291044776119406', '0.0', '5.0',
        '20.41153916783217', '35.15095384615384', '33.06700419580419',
        '0.030012394405594407', '0.03883611188811189',
        '33.92974545454545', '2.8697482027972026', '4.989835524475523',
        '6.264219707374398', '0.5195554230769229', '0.8367766153846156',
        '7.9836746812928245', '20.31116100975422', '43.0',
        '26.28790241305602', '6.0', '8.635014764160056',
        '105.17290502532907', '2.258065118171848', '2.6566957476791404',
        '6.919303657107979', '23.69289221631156', '69.51447392086176\n'],
['44', 'GA', '5056.147286821705', '631.4883720930233', '',
        '50.56147286821705', '63.14883720930233', '10', '10', 'georgia',
        'GA', '16', '3', '57.38867924528302', '11.0', '192.0',
        '21.09714135142858', '37.34693571428571', '35.26785',
        '0.028740961428571424', '0.04141132142857143',
        '35.52217142857143', '2.656933647142857', '4.853962142857141',
        '5.43288671349426', '0.5598400800000002', '0.8777667142857142',
        '8.273645191582537', '21.124138333412066', '537.0',
        '26.214098097928233', '5.0', '4.493650745524522',
        '104.32813920528623', '3.0658064337376074', '3.2013823730071684',
        '9.433399157974948', '25.90994516140285', '62.67941163471923\n'],
['45', 'MS', '5788.315789473684', '635.4526315789474', '',
        '57.88315789473684', '63.54526315789474', '24', '24',
        'mississippi', 'MS', '37', '7', '66.97439024390242', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '\n'],
['46', 'TX', '3117.4016736401672', '656.1610878661088', '',
        '31.174016736401672', '65.61610878661088', '43', '43', 'texas',
        'TX', '80', '37', '7.663385826771656', '41.0', '702.0',
        '12.176066710604038', '26.527206608607287', '25.013198446334464',
        '0.025935293743639287', '0.03883930523028648',
        '33.249364980589306', '0.6921662770590429', '1.857039655882449',
        '2.4792741491518537', '0.26981745434648097',
        '0.5054190680005104', '4.553036889142978', '16.323718616304646',
        '1896.0', '26.49934704143848', '7.0', '10.428616964835866',
        '167.81253772033986', '4.557568820885071', '5.468081051985687',
        '13.237394696970506', '39.026374871775495',
        '105.46941189356238\n'],
['47', 'LA', '5916.9607843137255', '666.7254901960785', '',
        '59.16960784313726', '66.67254901960784', '18', '18',
        'louisiana', 'LA', '35', '7', '69.29218750000003', '19.0',
        '328.0', '13.325842989168274', '26.624678911694552',
        '25.126369376104854', '0.02151748088564625',
        '0.03491953134645608', '29.80883674200777', '1.5901204761175365',
        '3.693189858453157', '4.743816580017097', '0.4516881693383813',
        '0.6349727418462253', '5.820614698588687', '16.374909349179607',
        '912.0', '25.986850016948907', '7.0', '3.3916110932432013',
        '57.08880820476962', '1.315439322354191', '1.8041391345986917',
        '4.2900335721549885', '12.475154780161128',
        '37.150716416918186\n'],
['48', 'HI', '5330.357142857143', '715.0', '',
        '53.30357142857143', '71.5', '11', '11', 'hawaii', 'HI', '2',
        '0', '-192.18', '12.0', '209.0', '15.454481350972788',
        '27.464856448827664', '25.999798910165392',
        '0.034534621789017256', '0.04185971898384454',
        '35.832890778617745', '2.757365300088262', '4.376870522276373',
        '5.285328439457492', '0.5358828355846326', '0.7658921895698186',
        '7.563752828855883', '18.67044273927413', '592.0',
        '26.69955589073236', '9.0', '5.66830934921945',
        '73.61086308817995', '1.5380645041438603', '1.2707497367597256',
        '3.512856283458392', '13.205257651359204', '54.07542821998982\n'],
['49', 'FL', '5446.689873417721', '721.9113924050633', '',
        '54.466898734177214', '72.19113924050633', '9', '9', 'florida',
        'FL', '36', '33', '66.70447761194032', '10.0', '175.0',
        '8.293475795688696', '19.10040412403556', '17.996695789960143',
        '0.02569452697310038', '0.0392611266631788', '33.54320100197837',
        '0.5199800512377353', '1.8381783810176795', '2.6208645464697167',
        '0.40484089606679424', '0.5590890837160913', '5.657569293913458',
        '14.954582658080422', '482.0', '26.540053513756376', '5.0',
        '7.360109238008545', '126.38541057390054', '2.5289641692636446',
        '3.2873640304111', '9.356048701260669', '27.68133550921617',
        '83.44616222217384\n']]


    climate_data = np.array(data)
    try:
        columns = json.loads(event['body'])
    except:
        columns = ["Storm Injuries","Pneumonea/Flu Deaths","Temperature","Storm Deaths","Lung Cancer Deaths","Precipitation"]

    final = parse_data(climate_data,columns)
    return {
        'statusCode': 200,
        'body': json.dumps(final)
    }