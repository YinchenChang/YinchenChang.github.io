/**
 * 網站留言板＋造訪計數器（Google Apps Script；綁定在 Drive「網站留言與造訪」試算表）
 * 留言：讀者在 yinchenchang.github.io 的留言板頁或文章底部留言，寫進「留言」頁；網站讀回「狀態」不是「隱藏」的留言。
 * 造訪：每次開啟頁面送一筆到「造訪紀錄」頁；「造訪彙總」頁用公式統計（總計、近 60 天、熱門頁面）。只記錄，不在網站顯示。
 * 不需讀者登入；不收 IP、不用 cookie。訪客代號是瀏覽器端隨機產生、只存在讀者自己的瀏覽器，只用來限制連續送出。
 *
 * 安裝（一次）：試算表 → 擴充功能 → Apps Script → 整段貼上 → 儲存 → 部署 → 新增部署作業
 *       → 類型「網頁應用程式」→ 執行身分「我」、存取權「任何人」→ 部署 → 授權 → 複製網址交給 Claude。
 * 管理：
 *   - 隱藏一則留言：把該列「狀態」改成「隱藏」（網站立即不再顯示，資料仍保留）。
 *   - 回覆：在該列「作者回覆」欄寫字，網站會顯示在留言下方，標為作者回覆。
 *   - 新留言寄信通知：把下方 NOTIFY 改成 true，存檔後「管理部署作業 → 編輯 → 新版本」。
 * 權威位置：YinchenChang.github.io/tools/comments/Code.gs（改版改這裡，再貼回 Apps Script 並發布新版本）。
 */
var TZ = 'Asia/Taipei';
var SHEET = '留言';
var HEAD = ['時間（台北）', '討論串', '頁面標題', '暱稱', '內容', '語言', '訪客代號', '狀態', '作者回覆'];
var NOTIFY = false;          // true：每則新留言寄一封信到試算表擁有者信箱
var MAX_TEXT = 2000;         // 每則上限字數
var GAP_SEC = 30;            // 同一訪客兩則留言最短間隔
var DAY_CAP = 300;           // 全站每天上限（防灌水）

var LOG = '造訪紀錄';
var SUM = '造訪彙總';
var LOG_HEAD = ['時間（台北）', '日期', '頁面', '語言', '訪客代號', '來源網站', '裝置', '螢幕寬'];

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.ev === 'view') return view_(p);
  var thread = clip_(p.thread, 120);
  var sh = ensure_(SpreadsheetApp.getActiveSpreadsheet());
  var n = sh.getLastRow() - 1;
  var rows = n > 0 ? sh.getRange(2, 1, n, HEAD.length).getDisplayValues() : [];
  var list = [];
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i];
    if (r[7] === '隱藏') continue;
    if (thread && r[1] !== thread) continue;
    list.push({ t: r[0], thread: r[1], title: r[2], name: r[3], text: r[4], reply: r[8] });
  }
  list = list.slice(-300);
  return json_({ ok: true, comments: list });
}

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.hp) return json_({ ok: true });                          // 機器人填了隱藏欄位：假裝成功、不寫入
  var text = String(p.text || '').trim();
  if (text.length < 2 || text.length > MAX_TEXT) return json_({ ok: false, err: 'length' });
  var vid = clip_(p.vid, 40);
  var cache = CacheService.getScriptCache();
  if (vid && cache.get('v' + vid)) return json_({ ok: false, err: 'too_fast' });
  var day = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
  var cnt = Number(cache.get('d' + day) || 0);
  if (cnt >= DAY_CAP) return json_({ ok: false, err: 'cap' });

  var lock = LockService.getScriptLock();
  lock.tryLock(5000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ensure_(ss);
    var row = ["'" + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'),
               clip_(p.thread, 120), clip_(p.title, 120), clip_(p.name, 40) || '訪客',
               safe_(text.slice(0, MAX_TEXT)), clip_(p.lang, 5), vid, '顯示', ''];
    sh.appendRow(row);
    if (NOTIFY) {
      MailApp.sendEmail(ss.getOwner().getEmail(), '網站新留言：' + row[2],
                        row[3] + '：\n\n' + text + '\n\n' + ss.getUrl());
    }
  } finally {
    lock.releaseLock();
  }
  if (vid) cache.put('v' + vid, '1', GAP_SEC);
  cache.put('d' + day, String(cnt + 1), 21600);
  return json_({ ok: true });
}

function view_(p) {
  var lock = LockService.getScriptLock();
  lock.tryLock(5000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(LOG) || setupLog_(ss);
    var now = new Date();
    sh.appendRow(["'" + Utilities.formatDate(now, TZ, 'yyyy-MM-dd HH:mm:ss'), "'" + Utilities.formatDate(now, TZ, 'yyyy-MM-dd'),
                  clip_(p.path, 160), clip_(p.lang, 5), clip_(p.vid, 40), clip_(p.ref, 120), clip_(p.dev, 10), clip_(p.w, 6)]);
  } finally {
    lock.releaseLock();
  }
  return json_({ ok: true });
}

function setupLog_(ss) {
  var sh = ss.insertSheet(LOG);
  sh.getRange(1, 1, 1, LOG_HEAD.length).setValues([LOG_HEAD]).setFontWeight('bold');
  sh.setFrozenRows(1);
  buildSummary_(ss);
  return sh;
}

/** 重建「造訪彙總」頁公式（在編輯器選此函式按「執行」；不動紀錄）。 */
function rebuildSummary() { buildSummary_(SpreadsheetApp.getActiveSpreadsheet()); }

function buildSummary_(ss) {
  var s = ss.getSheetByName(SUM) || ss.insertSheet(SUM);
  s.clear();
  var L = "'" + LOG + "'!";
  s.getRange('A1').setValue('總計').setFontWeight('bold');
  s.getRange('A2:A4').setValues([['瀏覽次數'], ['不重複訪客'], ['留言數']]);
  s.getRange('B2').setFormula('=COUNTA(' + L + 'C2:C)');
  s.getRange('B3').setFormula('=IFERROR(ROWS(UNIQUE(FILTER(' + L + 'E2:E,' + L + 'E2:E<>""))),0)');
  s.getRange('B4').setFormula("=MAX(COUNTA('" + SHEET + "'!A2:A),0)");
  s.getRange('A6:C6').setValues([['日期', '瀏覽次數', '不重複訪客']]).setFontWeight('bold');
  var f = [];
  for (var i = 0; i < 60; i++) {
    var r = 7 + i, d = 'TEXT($A' + r + ',"yyyy-mm-dd")';
    f.push(['=TODAY()-' + i, '=COUNTIF(' + L + 'B2:B,' + d + ')',
            '=IFERROR(ROWS(UNIQUE(FILTER(' + L + 'E2:E,' + L + 'B2:B=' + d + '))),0)']);
  }
  s.getRange(7, 1, 60, 3).setFormulas(f);
  s.getRange(7, 1, 60, 1).setNumberFormat('yyyy-mm-dd');
  s.getRange('E1').setValue('熱門頁面（前 30）').setFontWeight('bold');
  s.getRange('E2').setFormula('=IFERROR(QUERY(' + L + 'C2:C,"select C, count(C) where C is not null group by C order by count(C) desc limit 30 label C \'頁面\', count(C) \'瀏覽\'",0),"尚無資料")');
  s.getRange('H1').setValue('來源網站（前 20）').setFontWeight('bold');
  s.getRange('H2').setFormula('=IFERROR(QUERY(' + L + 'F2:F,"select F, count(F) where F is not null and F <> \'\' group by F order by count(F) desc limit 20 label F \'來源\', count(F) \'次數\'",0),"尚無資料")');
  s.setColumnWidth(1, 100); s.setColumnWidth(5, 320); s.setColumnWidth(8, 220);
}

// 單行欄位：去掉換行與定位字元，開頭的 = + - @ 前面加 '，避免被試算表當成公式
function clip_(s, n) { return String(s == null ? '' : s).replace(/[\r\n\t]/g, ' ').replace(/^[=+\-@]/, "'$&").trim().slice(0, n); }
// 內容欄位：保留換行，只防公式
function safe_(s) { return String(s).replace(/\r/g, '').replace(/^[=+\-@]/, "'$&"); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/** 建立「留言」「造訪紀錄」「造訪彙總」三頁（部署前在編輯器選 setup 按「執行」一次；之後收到資料也會自動建立）。 */
function setup() { var ss = SpreadsheetApp.getActiveSpreadsheet(); ensure_(ss); if (!ss.getSheetByName(LOG)) setupLog_(ss); }

function ensure_(ss) {
  var sh = ss.getSheetByName(SHEET);
  if (sh) return sh;
  ss.setSpreadsheetTimeZone(TZ);
  sh = ss.insertSheet(SHEET, 0);
  sh.getRange(1, 1, 1, HEAD.length).setValues([HEAD]).setFontWeight('bold');
  sh.setFrozenRows(1);
  sh.setColumnWidth(5, 420); sh.setColumnWidth(9, 280);
  sh.getRange('H2:H').setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(['顯示', '隱藏'], true).build());
  return sh;
}
