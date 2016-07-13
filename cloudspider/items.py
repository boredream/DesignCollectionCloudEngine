# -*- coding: utf-8 -*-

class UiItem():
    # 名称
    name = ''

    # 图片链接
    imgUrl = ''

    # 描述
    desc = ''

    # 来源网站名称
    srcTag = ''

    # 源链接
    srcLink = ''

    # 是否已经添加到服务器
    isAdd = ''

    def __init__(self, name, imgUrl, desc, srcTag, srcLink, isAdd):
        self.name = name
        self.imgUrl = imgUrl
        self.desc = desc
        self.srcTag = srcTag
        self.srcLink = srcLink
        self.isAdd = isAdd
