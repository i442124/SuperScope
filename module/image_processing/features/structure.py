import cv2
from skimage.metrics import normalized_root_mse
from skimage.metrics import structural_similarity

# the default width of an image
# when extracting the image strucutre
# must match size configured in the data storage solution
DEFAULT_STRUCTURAL_WIDTH = 16

# the default height of an image
# when extracting the image structure
# must match size configured in the data storage solution
DEFAULT_STRUCTURAL_HEIGHT = 16

# normalization method used for RMSE
# possible choises: ['euclidean','min-max', 'mean']
NORMALIZATION_METHOD = 'min-max'

# extract the structure of an image
# by downscaling the image first
def extract_from_image(image,
    width=DEFAULT_STRUCTURAL_WIDTH,
    height=DEFAULT_STRUCTURAL_HEIGHT):
    return cv2.resize(image, (width, height))

# compare the similarity between images using
# structural_similarity (also known as SSIM)
def compare_ssim(IMG1, IMG2, multichannel=True):
    return structural_similarity(IMG1, IMG2, multichannel)

# compare the similarity between images using
# normalized_root_mse (also known as NRMSE)
def compare_nrmse(IMG1, IMG2, normalization=NORMALIZATION_METHOD):
    return normalized_root_mse(IMG1, IMG2, normalization=normalization)
