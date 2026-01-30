
def predict_gen(meta1):
    import pickle
    import os
    import numpy as np
    from django.conf import settings
    path = os.path.join(settings.MODELS, 'models.p')
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled, encoding='latin1')
    svmp = data['svmp']
    norma = data['norma']
    lgn = data['lgn']
    
    # Fix missing attributes in old sklearn models
    if not hasattr(svmp, '_probA'):
        svmp._probA = np.array([])
    if not hasattr(svmp, '_probB'):
        svmp._probB = np.array([])
    if not hasattr(norma, 'clip'):
        norma.clip = False
    
    # Convert meta1 to numpy array and ensure proper shape
    meta_array = np.array(meta1).reshape(1, -1)
    
    # Manually normalize if scaler has issues
    try:
        x = norma.transform(meta_array)
    except AttributeError:
        # Fallback: manual normalization
        if hasattr(norma, 'data_min_') and hasattr(norma, 'data_range_'):
            x = (meta_array - norma.data_min_) / norma.data_range_
        else:
            x = meta_array
    
    pred = svmp.predict(x)
    return(lgn[pred[0]])

