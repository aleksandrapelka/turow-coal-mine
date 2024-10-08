def get_breaks():
    return {
        'NDWI_I': [-1.0,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0],
        'NDWI_II': [-1.0,-0.8,-0.6,-0.5,-0.4,-0.2,0.0,0.2,0.5,0.8,1.0],
        'NDVI': [-1.0,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0],
        'MSAVI2': [-5.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,5.0],
        'EVI': [-100.0,0.0,0.4,0.8,1.2,1.6,2.0,2.4,3.8,4.2,100.0],
        'NMDI': [-5.0,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,5.0],
        'MSI': [0.0,0.2,0.4,0.5,0.8,1.0,1.5,2.0,3.0,4.0,6.0]
    }


def get_palette():
    return {
        'NDWI_I': ["#8B0000", "#962A2A", "#A15454", "#AD7E7E", "#B8A8A8", "#ACB2B9", "#889CB0", "#6585A6", "#416E9D", "#1E5894"], #RdBl
        'NDWI_II': ["#888888", "#959595", "#B5B5B5", "#D2D2D2", "#E2E2E2", "#F4F4F4", "#9CDBF3", "#4DADDB", "#217BB6", "#1E5894"], #GyBl
        'NDVI': ["#8B0000", "#A03323", "#B66647", "#CC996B", "#E2CC8F", "#D2D790", "#9EBA6C", "#699D48", "#348024", "#006400"], #RdYlGn
        'MSAVI2': ["#CB1212", "#D24132", "#DA7051", "#E19F71", "#E9CE92", "#D2D790", "#9EBA6C", "#699D48", "#348024", "#006400"], #RdGn
        'EVI': ["#F5F5F5", "#CCD7CC", "#A4BAA4", "#8CAE8C", "#75A175", "#5D955D", "#357835", "#1D6B1D", "#066006", "#004200"], #Gn
        'NMDI_temp': ["#1E5894", "#507BA8", "#82A0BD", "#B3C3D2", "#E5E7E7", "#F2ECE4", "#D9D2C9", "#BFB7AD", "#A69D92", "#8D8377"], #BrBl
        'NMDI': ["#4b4443", "#6D6665", "#8F8887", "#B7B0A7", "#F2ECE4", "#E5E7E7", "#91A1B0", "#60809B", "#305986", "#0C3672"], #BlBr
        'MSI': ["#283137","#2e4249","#3a656d","#478891","#53aab5","#5fcdd9", "#B8A8A8", "#AD7E7E", "#A15454", "#9C1111"],
        #'line_chart': ["#ebf7fa", "#5fcdd9", "#478891"], # for dark
        'line_chart': ["#333333", "#478891", "#5fcdd9"], # for light
        #'multi_year_chart': ['#259ebb',"#8B0000","#4ab7d1",'#61b6ca',"#afdfeb","#d7eff5", "#CCD7CC"], # for dark
        'multi_year_chart': ['#037c99',"#9C0000",'#259ebb','#888888',"#5fcdd9","#666666", "#C37676"], # for light
        'multi_year_histogram': "#5fcdd9",
        'changes': ['#962A2A', "#AD7E7E", "#5fcdd9", "#53aab5"]
    }


def get_vis_params():
    palette = get_palette()
    breaks = get_breaks()

    vis_params = {
        'NDWI_I': {'min': 1, 'max': 10, 'palette': palette['NDWI_I'], 'breaks': breaks['NDWI_I']},
        'NDWI_II': {'min': 1, 'max': 10, 'palette': palette['NDWI_II'], 'breaks': breaks['NDWI_II']},
        'NDVI': {'min': 1, 'max': 10, 'palette': palette['NDVI'], 'breaks': breaks['NDVI']},
        'MSAVI2': {'min': 1, 'max': 10, 'palette': palette['MSAVI2'], 'breaks': breaks['MSAVI2']},
        'EVI': {'min': 1, 'max': 10, 'palette': palette['EVI'], 'breaks': breaks['EVI']},
        'NMDI': {'min': 1, 'max': 10, 'palette': palette['NMDI'], 'breaks': breaks['NMDI']},
        'MSI': {'min': 1, 'max': 10, 'palette': palette['MSI'], 'breaks': breaks['MSI']},
        'changes': {'min': 1, 'max': 4, 'palette': palette['changes']}
    }

    return vis_params


def get_labels():
    return {
        'NDWI_I': ['-1.0 - 0.0','0.0 - 0.1','0.1 - 0.2','0.2 - 0.3','0.3 - 0.4','0.4 - 0.5','0.5 - 0.6','0.6 - 0.7','0.7 - 0.8','0.8 - 1.0'],
        'NDWI_II': ['-1.0 - -0.8','-0.8 - -0.6','-0.6 - -0.5','-0.5 - -0.4','-0.4 - -0.2','-0.2 - 0.0','0.0 - 0.2','0.2 - 0.5','0.5 - 0.8','0.8 - 1.0'],
        'NDVI': ['-1.0 - -0.1','-0.1 - 0.1','0.1 - 0.2','0.2 - 0.3','0.3 - 0.4','0.4 - 0.5','0.5 - 0.6','0.6 - 0.7','0.7 - 0.8','0.8 - 1.0'],
        'MSAVI2': ['-5.0 - -0.8','-0.8 - -0.6','-0.6 - -0.4','-0.4 - -0.2','-0.2 - 0.0','0.0 - 0.2','0.2 - 0.4','0.4 - 0.6','0.6 - 0.8','0.8 - 5.0'],
        'EVI': ['-100.0 - 0.0','0.0 - 0.4','0.4 - 0.8','0.8 - 1.2','1.2 - 1.6','1.6 - 2.0','2.0 - 2.4','2.4 - 3.8','3.8 - 4.2','4.2 - 100.0'],
        'NMDI': ['-5.0 - 0.0','0.0 - 0.1','0.1 - 0.2','0.2 - 0.3','0.3 - 0.4','0.4 - 0.5','0.5 - 0.6','0.6 - 0.7','0.7 - 0.8','0.8 - 5.00'],
        'MSI': ['0.0 - 0.2', '0.2 - 0.4', '0.4 - 0.5', '0.5 - 0.8', '0.8 - 1.0', '1.0 - 1.5', '1.5 - 2.0', '2.0 - 3.0', '3.0 - 4.0', '4.0 - 6.0'],
        'changes': ['Strong Negative Changes', 'Negative Changes', 'Positive Changes', 'Strong Positive Changes']
    }