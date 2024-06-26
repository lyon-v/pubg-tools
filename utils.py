import cv2
import numpy as np
import os


def preprocess_image_for_white_objects(image):
    """ 提取亮白色物体 """
    # 转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 设定白色的阈值范围，调整这些阈值以只包含亮白色区域
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 30, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # 使用膨胀操作让物体区域更加明显
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask



def find_most_similar_old(target_images, search_image, search_region_coords):
    """ 在给定区域内找到与目标图像最相似的图像，并返回最相似目标的轮廓信息和矩形框 """
    x, y, w, h = search_region_coords
    search_region = search_image[y:y+h, x:x+w]
    mask = preprocess_image_for_white_objects(search_region)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_match = None
    max_similarity = -1
    guns_name = None
    best_contour = None
    best_rect = None

    for name, target_img in target_images.items():
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            candidate = search_region[y:y+h, x:x+w]
            candidate_gray = cv2.cvtColor(candidate, cv2.COLOR_BGR2GRAY)

            shape_similarity = cv2.matchShapes(target_gray, candidate_gray, cv2.CONTOURS_MATCH_I1, 0)
            # print("similarity ==> ",shape_similarity)
            if shape_similarity < max_similarity or max_similarity == -1:
                max_similarity = shape_similarity
                best_match = candidate
                guns_name = name
                best_contour = cnt
                best_rect = ( x, y, w, h)
                 

    return guns_name, best_contour,best_rect,max_similarity,best_match



def find_most_similar(target_images, search_image, search_region_coords):
    # 处理搜索区域
    x, y, w, h = search_region_coords
    search_region = search_image[y:y+h, x:x+w]
    search_region_mask = preprocess_image_for_white_objects(search_region)
    search_contours, _ = cv2.findContours(search_region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 初始化最佳匹配变量
    best_match = None
    max_similarity = -1
    best_name = None
    best_contour = None
    best_rect = None

    # 处理目标图像，计算每个图像的轮廓
    target_contours = {}
    for name, target_img in target_images.items():
        mask = preprocess_image_for_white_objects(target_img)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 找到面积最大的轮廓
        max_contour = max(contours, key=cv2.contourArea)
    
        target_contours[name] = max_contour #contours[0]  # 假设每个目标图像中只有一个显著轮廓

    search_cnt = max(search_contours, key=cv2.contourArea)
    # 比较轮廓
    for name, target_cnt in target_contours.items():
     
        shape_similarity = cv2.matchShapes(target_cnt, search_cnt, cv2.CONTOURS_MATCH_I1, 0)
        if shape_similarity < max_similarity or max_similarity == -1:
            max_similarity = shape_similarity
            best_match = search_cnt
            best_name = name
            best_rect = cv2.boundingRect(best_match)
    
    # 返回最佳匹配的目标图像名、轮廓、边界矩形和相似度
    return best_name, best_contour, best_rect, max_similarity, best_match


def draw_contour(image, contour, offset, color=(0, 255, 0), thickness=2):
    """ 在图像上绘制轮廓 """
    # 因为轮廓是在搜索区域中找到的，需要加上偏移量来画在原始图像上
    shifted_contour = contour.copy()
    shifted_contour[:, :, 0] += offset[0]  # X offset
    shifted_contour[:, :, 1] += offset[1]  # Y offset
    cv2.drawContours(image, [shifted_contour], -1, color, thickness)
    
    
def draw_rectangle(image, rect, color=(0, 255, 0), thickness=2):
    """ 在图像上绘制矩形 """
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    
 
 
def showContours(image, contours, offset): 
    
    for cnt  in contours:
        draw_contour(image, cnt, offset)
        
    cv2.imshow("Matched Result with Contour", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
 
def SplitVideo(videopath, ratio=30 ,savedir=""):
    
    if savedir =="" or videopath=="":
        return 
    
    # videopath = 'D:\\wuliang\\Aworkspace\\pyw\\video\\guns_test.mp4'

    vc = cv2.VideoCapture(videopath)  # import video files
    # determine whether to open normally
    if vc.isOpened():
        ret, frame = vc.read()
    else:
        ret = False
    
    count = 0  # count the number of pictures
    videoname = os.path.basename(videopath).split(".")[0]
    # loop read video frame
    while ret:
        ret, frame = vc.read()
        count += 1
        if count %ratio==0:
            
            imagename = videoname+"_"+str(count)+".jpg"
            impath = os.path.join(savedir,imagename)
            
            cv2.imwrite(impath, frame)
            
            print(impath,"==> done")

    vc.release()

 
if __name__ == "__main__":
    
    videopath = 'D:\\wuliang\\Aworkspace\\pyw\\video\\guns_test.mp4'
    SplitVideo(videopath,30,"../pubgimgs")