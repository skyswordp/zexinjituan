const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function addBookmarks() {
  const pdfPath = 'c:/Users/DEVTrump/projects/docs-1/friend/Friend-Circle-API-v1.0.pdf';
  const pdfBytes = fs.readFileSync(pdfPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);

  const totalPages = pdfDoc.getPageCount();
  console.log('Total pages:', totalPages);

  // 读取每一页的文本来定位章节位置
  // pdf-lib 不支持读取文本，所以我们根据已知的 PDF 内容手动标记页码
  // 基于之前查看的 PDF 内容（21页）：
  const bookmarks = [
    { title: '朋友圈产品交互文档', page: 0 },
    { title: '目录', page: 0 },
    { title: '架构总览', page: 0 },
    { title: '接口规范', page: 0 },
    { title: '1. 个人中心模块', page: 1, children: [
      { title: '1.1 getUser - 获取用户资料', page: 1 },
      { title: '1.2 update - 更新用户资料', page: 3 },
      { title: '1.3 getMyPraiseCount - 获取消息计数', page: 4 },
      { title: '1.4 getLevel - 获取等级权限', page: 4 },
    ]},
    { title: '2. 社交关系模块', page: 5, children: [
      { title: '2.1 saveFollow - 关注/取消关注', page: 5 },
    ]},
    { title: '3. 朋友圈动态模块', page: 6, children: [
      { title: '3.1 saveCircle - 发布动态', page: 6 },
      { title: '3.2 pageList - 动态列表', page: 7 },
      { title: '3.3 readCount - 阅读计数', page: 9 },
      { title: '3.4 getCountList - 获取统计', page: 10 },
    ]},
    { title: '4. 互动功能模块', page: 10, children: [
      { title: '4.1 saveChangePraise - 点赞/取消点赞', page: 10 },
      { title: '4.2 saveComments - 发表评论', page: 11 },
      { title: '4.3 pageList - 评论列表', page: 12 },
      { title: '4.4 saveShare - 分享', page: 13 },
      { title: '4.5 saveReport - 举报', page: 14 },
    ]},
    { title: '5. 话题广场模块', page: 14, children: [
      { title: '5.1 queryTitle - 话题列表', page: 14 },
      { title: '5.2 queryDetails - 话题详情', page: 15 },
    ]},
    { title: '6. 任务中心模块', page: 16, children: [
      { title: '6.1 queryTasks - 任务列表', page: 16 },
    ]},
    { title: '7. 板块功能模块', page: 17, children: [
      { title: '7.1 index/getByLevel - 首页板块', page: 17 },
      { title: '7.2 guess/getByLevel - 猜你喜欢', page: 18 },
    ]},
    { title: '8. 配置管理模块', page: 18, children: [
      { title: '8.1 indexSetting/pageList - 首页配置', page: 18 },
      { title: '8.2 gameSetting/pageList - 游戏配置', page: 19 },
    ]},
    { title: '接口清单', page: 19 },
    { title: '附录：实体类源码位置', page: 20 },
  ];

  // pdf-lib 不直接支持 outline bookmarks，需要手动构建 PDF outline 字典
  const { PDFName, PDFDict, PDFArray, PDFString, PDFRef, PDFNumber } = require('pdf-lib');
  const context = pdfDoc.context;

  function createDest(pageIndex) {
    const pageRef = pdfDoc.getPage(Math.min(pageIndex, totalPages - 1)).ref;
    const destArray = context.obj([pageRef, PDFName.of('Fit')]);
    return destArray;
  }

  // 扁平化书签，构建链表
  let allItems = [];

  for (let i = 0; i < bookmarks.length; i++) {
    const bm = bookmarks[i];
    const item = {
      title: bm.title,
      page: bm.page,
      children: bm.children || [],
      ref: null,
    };
    allItems.push(item);
  }

  // 构建 outline items（先构建子项，再构建父项）
  function buildOutlineItems(items, parentRef) {
    const refs = [];

    for (let i = 0; i < items.length; i++) {
      const ref = context.nextRef();
      items[i].ref = ref;
      refs.push(ref);
    }

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const dict = context.obj({
        Title: PDFString.of(item.title),
        Parent: parentRef,
        Dest: createDest(item.page),
      });

      if (i > 0) dict.set(PDFName.of('Prev'), refs[i - 1]);
      if (i < items.length - 1) dict.set(PDFName.of('Next'), refs[i + 1]);

      // 处理子项
      if (item.children && item.children.length > 0) {
        const childRefs = buildOutlineItems(item.children, refs[i]);
        dict.set(PDFName.of('First'), childRefs[0]);
        dict.set(PDFName.of('Last'), childRefs[childRefs.length - 1]);
        dict.set(PDFName.of('Count'), PDFNumber.of(item.children.length));
      }

      context.assign(refs[i], dict);
    }

    return refs;
  }

  // 创建 Outlines 根字典
  const outlinesRef = context.nextRef();
  const topRefs = buildOutlineItems(allItems, outlinesRef);

  const outlinesDict = context.obj({
    Type: PDFName.of('Outlines'),
    First: topRefs[0],
    Last: topRefs[topRefs.length - 1],
    Count: PDFNumber.of(allItems.length),
  });

  context.assign(outlinesRef, outlinesDict);

  // 设置到 catalog
  const catalog = pdfDoc.catalog;
  catalog.set(PDFName.of('Outlines'), outlinesRef);
  catalog.set(PDFName.of('PageMode'), PDFName.of('UseOutlines')); // 默认打开时显示书签

  const modifiedPdfBytes = await pdfDoc.save();
  fs.writeFileSync(pdfPath, modifiedPdfBytes);
  console.log('Done! Bookmarks added to', pdfPath);
}

addBookmarks().catch(console.error);
