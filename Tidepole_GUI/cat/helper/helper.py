import numpy as np
import cv2
import imutils


def click(event, x, y, flags, param):
    global point, pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed",x,y)
        point = (x,y)
        return point


def mask_frame(frame, bounds):
    for (lower, upper) in bounds:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)
        return output


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour, area_min, area_max):



    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #areaMin = cv2.getTrackbarPos("Area", "Parameters")
        areaMin = area_min
        area_max = area_max

        if area > areaMin:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            scaling_num = 7
            x = x + scaling_num
            y = y + scaling_num

            x_p = x + w - 2*scaling_num
            y_p = y + h - 2*scaling_num
            cv2.rectangle(imgContour, (x , y ), (x_p , y_p), (0, 255, 0), 5)

            cv2.putText(imgContour, "LCD Detected: ", (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 1.2,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            print('area', area)
            #This is a bit sketchy, but should work for now...entire structure and dependencies should be reviewed
            return x, y, x_p, y_p
        # else:
        #     print('here')
        #
        #     return 0, 0, 0, 0


def getContours2(img,imgContour, area_min, area_max):



    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    for cnt in contours:
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, arclen * 1, True)
        # drawContours
        cv2.drawContours(imgContour, [approx], -1, (0, 0, 255), 1, cv2.LINE_AA)
        # area = cv2.contourArea(cnt)
        # #areaMin = cv2.getTrackbarPos("Area", "Parameters")
        # areaMin = area_min
        # area_max = area_max

        # if area > areaMin:
        #     cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
        #     peri = cv2.arcLength(cnt, True)
        #     approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        #     print(len(approx))
        #     x , y , w, h = cv2.boundingRect(approx)
        #     scaling_num = 0
        #     x = x + scaling_num
        #     y = y + scaling_num
        #
        #     x_p = x + w - 2*scaling_num
        #     y_p = y + h - 2*scaling_num
        #     cv2.rectangle(imgContour, (x , y ), (x_p , y_p), (0, 255, 0), 5)
        #
        #     cv2.putText(imgContour, "LCD Detected: ", (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 1.2,
        #                 (0, 255, 0), 2)
        #     cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
        #                 (0, 255, 0), 2)
        #     #This is a bit sketchy, but should work for now...entire structure and dependencies should be reviewed
        #     print('x, y, x_p, y_p', x, y, x_p, y_p)
        #     return x, y, x_p, y_p


def multi_scale_tm(img, template_img):
    # load the image image, convert it to grayscale, and detect edges
    template = template_img
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    # cv2.imshow("Template", template)

    # loop over the images to find the template in
    found = None
    image = img
    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(image, width = int(image.shape[1] * scale))
        r = image.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        #edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # check to see if the iteration should be visualized
        # if args.get("visualize", False):
        # draw a bounding box around the detected region
        clone = np.dstack([resized, resized, resized])
        cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
            (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
        cv2.imshow("Visualize", clone)
        cv2.waitKey(0)

        # if we have found a new maximum correlation value, then ipdate
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    # unpack the bookkeeping varaible and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

    # draw a bounding box around the detected result and display the image
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)

