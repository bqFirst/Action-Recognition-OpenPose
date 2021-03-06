# coding=utf8


class actionPredictor(object):

    def __init__(self):
        pass

    @staticmethod
    def move_status(joints):

        # 第一帧 颈 右腰 左腰（人体起始帧中心）
        init_x = float(joints[0][1][0] + joints[0][8][0] + joints[0][11][0]) / 3
        init_y = float(joints[0][1][1] + joints[0][8][1] + joints[0][11][1]) / 3
        # 最后一帧 颈 右腰 左腰（人体终止帧中心）
        end_x = float(joints[-1][1][0] + joints[-1][8][0] + joints[-1][11][0]) / 3
        end_y = float(joints[-1][1][1] + joints[-1][8][1] + joints[-1][11][1]) / 3

        # 起始帧腰到脖子垂直距离
        init_h1 = float(joints[0][8][1] + joints[0][11][1]) / 2 - joints[0][1][1]
        # 终止帧腰到脖子垂直距离
        end_h1 = float(joints[-1][8][1] + joints[-1][11][1]) / 2 - joints[-1][1][1]
        try:
            h1 = end_h1 / init_h1  # 人体中心垂直运动比率 (终止 腰-脖子 / 起始 腰-脖子)
        except:
            h1 = 0.0
        # 起始帧 膝到腰垂直距离
        init_h2 = (float(joints[0][9][1] + joints[0][12][1]) - float(joints[0][8][1] + joints[0][11][1])) / 2
        # 终止帧 膝到腰垂直距离
        end_h2 = (float(joints[-1][9][1] + joints[-1][12][1]) - float(joints[-1][8][1] + joints[-1][11][1])) / 2
        try:
            h2 = end_h2 / init_h2  # 下肢垂直运动比率
        except:
            h2 = 0.0

        # 人体中心水平移动距离
        xc = end_x - init_x
        # 人体中心垂直移动距离
        yc = end_y - init_y
        if abs(xc) < 30. and abs(yc) < 20.:
            ty_1 = float(joints[-1][1][1])  # 终止帧脖子 y 坐标
            ty_8 = float(joints[-1][8][1] + joints[-1][11][1]) / 2  # 终止帧左右腰中心 y 坐标
            ty_9 = float(joints[-1][9][1] + joints[-1][12][1]) / 2  # 终止帧左右膝中心 y 坐标
            try:
                t = float(ty_8 - ty_1) / (ty_9 - ty_8)  # 终止帧 腰-脖子垂直距离 / 膝-脖子垂直距离
            except:
                t = 0.0
            if h1 < 1.16 and h1 > 0.84 and h2 < 1.16 and h2 > 0.84:

                if t < 1.73:
                    return 1
                else:
                    return 2
            else:
                if t < 1.7:
                    if h1 >= 1.08:
                        return 4

                    elif h1 < 0.92:
                        return 5
                    else:
                        return 0
                else:
                    return 0
        elif abs(xc) < 30. and abs(yc) >= 30.:
            init_y1 = float(joints[0][1][1])
            init_y8 = float(joints[0][8][1] + joints[0][11][1]) / 2
            init_y9 = float(joints[0][9][1] + joints[0][12][1]) / 2

            end_y1 = float(joints[-1][1][1])
            end_y8 = float(joints[-1][8][1] + joints[-1][11][1]) / 2
            end_y9 = float(joints[-1][9][1] + joints[-1][12][1]) / 2
            try:
                init_yc = float(init_y8 - init_y1) / (init_y9 - init_y8)
            except:
                init_yc = 0.0
            try:
                end_yc = float(end_y8 - end_y1) / (end_y9 - end_y8)
            except:
                end_yc = 0.0
            th_yc = 0.1
            if yc >= 25 and abs(end_yc - init_yc) >= th_yc:
                return 6
            elif yc < -20 and abs(end_yc - init_yc) >= th_yc:
                return 7
            else:
                return 0
        elif abs(xc) > 30. and abs(yc) < 30.:
            return 3
        else:
            return 0
