"""Generate a monochrome Meiryo UI workbook and the matching Japanese report."""
from __future__ import annotations

import json
import math
from pathlib import Path
import re
import unicodedata

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from PIL import ImageFont

import report_data as d

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
STEM = "ECS_Fargate_HealthCheck_詳細設計_20261012"
XLSX = OUT / f"{STEM}.xlsx"
MD = OUT / f"{STEM}.md"
FONT = "Meiryo UI"
REGULAR = ImageFont.truetype(r"C:\Windows\Fonts\meiryo.ttc", 15, index=2)

VERIFY_ROWS = [
    ["内容の照合", "ユーザー実測と仮定を分離。7パターン、4コンテナ、ECS猶予とALB設定の整合を検査。", "数値計算・JSONの構造をローカルで検証する。実AWSの受理・実行結果を意味しない。", "ローカル検証"],
    ["計算モデル", "P1はADOT38、バック準備180、複合API218、F HEALTHY233、通常完了263、追加予備込み323秒。設定猶予360秒。", "Excelに数式と初期計算結果を格納し、入力項目の検証範囲を設定。", "ローカル検証"],
    ["ファイル構造", "Excelは全セルMeiryo UI、モノトーン、折返し・行高・列幅・固定枠・印刷範囲・出典リンクを設定。MarkdownはUTF-8。", "自動検証の実行結果は同梱のvalidation.jsonに記録。表示はExcelの環境によりわずかに変わる場合がある。", "成果物"],
    ["表示と再計算の範囲", "Excelの自動操作はアプリ起動が応答しなかったため中断。実Excelでの再計算・印刷表示は未確認。", "数式と格納結果を独立計算で照合し、セル配置・行高・文字幅を使ったローカル描画で主要シートを確認する。", "制約と代替確認"],
    ["実環境未検証", "AWSへのログイン、CLI実行、実タスク配備、JBoss起動、readiness実装、トレース配送試験は行っていない。", "300秒の現物項目名、EAP版、イメージ内のコマンド、前後処理とサイドカー時間が未確定。", "制約"],
    ["設定例の限界", "タスク例は断片。/readyzと専用プローブは提案する実装契約。画像・権限・ネットワーク等を含む完全な配備定義ではない。", "特にCWの専用バイナリは未実装。現行の実行可能なプロセス検査があればそれを使う。", "制約"],
    ["Git検証", "作業フォルダーはGitリポジトリではないためgit diff --checkは利用できない。", "代替として作成ファイルの構文、末尾空白、改行、文字化けと出力内容を検査する。", "環境"],
    ["資料の数値の意味", "未実測値を含む設計予算であり、AWSのSLAや実際の最大起動時間ではない。", "観測条件が変われば21_秒数試算の入力を変更し、全パターンの採否を再検討する。", "前提"],
]


def refs_markdown(value):
    def repl(match):
        sid = match.group()
        title, url, _ = d.SOURCES[sid]
        return f"[{sid} {title}]({url})"
    return re.sub(r"S\d{2}", repl, str(value))


def md_table(headers, rows):
    def cell(v):
        return str(v).replace("|", "\\|").replace("\n", "<br>")
    lines = ["| " + " | ".join(map(cell, headers)) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        rendered = [cell(v) for v in row]
        rendered[-1] = refs_markdown(rendered[-1])
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def write_markdown():
    chunks = [
        "# ECS Fargate・ALB ヘルスチェックと起動依存の詳細設計",
        f"確認日：{d.CHECKED} ／ 対象：ECS Service・Linux Fargate・ALB・JBoss EAP・ADOT・CloudWatch Agent",
        "**第一候補はP1です。ADOTのHEALTHY後にバックを起動し、フロントは並列に開始します。フロント自身とバックの両方が使える時だけ正常を返す構成とし、startPeriodはADOT45・CW60・バック210・フロント240秒、ECSサービス猶予は360秒を初期案とします。** これはユーザーの160秒・140秒見積もりと、未実測の時間予算を分解して計算した結果です。仮定は実測で置き換えてください。",
        "`startPeriod=210`は検査開始を210秒遅らせません。ECSの300秒猶予もALBの初回検査を遅らせません。Fargateの依存先待ち`startTimeout`は最大120秒です。" + refs_markdown(" S01 S04 S05"),
        "## 読み方",
        "結論は第1章、設定値は第3・7・8章、バッファの秒数は第6章、経路の見直しは第11章です。第19章には全採用候補の設定断片、第21章には計算入力、第22章には時間軸を掲載します。Excelは同じ内容に加えて編集可能な試算とグラフを収録しています。",
        "**数値の区分**：実測＝ユーザー提供、ユーザー見積もり＝最大実測の2倍、仮定＝未計測部分の説明用予算、提案＝仮定込みの計算から選ぶ設定。既存のAWS設定ファイルは提供されていません。",
        "## 構成図：P1",
        '```mermaid\nflowchart LR\n  A["ADOT：13133で正常判定"] -->|HEALTHY依存| B["バック：JBoss EAP"]\n  F["フロント：独立して起動"] -. "readinessでAPIを確認" .-> B\n  C["CloudWatch Agent：独立して起動"]\n  L["ALB"] -->|タスクIP：フロントport /readyz| F\n  E["ECS：4つの必須コンテナとALBの状態を評価"]\n  A -. 状態 .-> E\n  B -. 状態 .-> E\n  F -. 状態 .-> E\n  C -. 状態 .-> E\n```',
        "図の実線は起動依存または外からの通信、点線は検査・状態参照です。フロントの検査がバックを参照しても、フロントプロセスの開始をバックHEALTHYまで遅らせることにはなりません。",
    ]
    for index, sec in enumerate(d.SECTIONS, 1):
        chunks += [f"## {index}. {sec['title']}", sec["intro"], md_table(sec["headers"], sec["rows"])]
    chunks += ["## 19. 設定例と実装の前提", md_table(["項目","説明","適用上の注意","根拠"],d.CONFIG_NOTES)]
    for p in d.PATTERNS:
        if p["id"] == "P4":
            continue
        chunks += [f"### {p['id']}：{p['name']}", f"{p['decision']}。ECSサービス猶予は **{p['grace']}秒**。ALB検査は共通の10秒／5秒／正常2回／異常3回です。", "```json\n"+json.dumps(d.task_fragment(p),ensure_ascii=False,indent=2)+"\n```"]
    chunks += ["### P1：ECSサービスの設定断片", "ECSローリング更新を前提とした例。必要なサービス識別子や既存の配備方式を省略しています。", "```json\n"+json.dumps(d.SERVICE_FRAGMENT,indent=2)+"\n```", "### ALBターゲットグループの設定断片", "新規作成・IaCにおける概念例。フロントHTTP8080を仮定し、VPC等は省略。既存環境のポートやTLSを優先して置換します。", "```json\n"+json.dumps(d.ALB_FRAGMENT,indent=2)+"\n```", "### ADOT：health extensionの設定断片", "```yaml\n"+d.ADOT_CONFIG+"\n```", "### バック用の厳密200プローブ例", "```sh\n"+d.BACKEND_SCRIPT+"\n```", "証明書の名前がlocalhostでない場合は、正しい証明書名のURLと`--resolve 証明書名:18080:127.0.0.1`等を使い、CA検証を保ちます。ここでのCAパスも配置前提の例です。", "### フロント用の複合readinessプローブ例", "```sh\n"+d.FRONTEND_SCRIPT+"\n```", "フロントの`/readyz`内でバックも短い期限で確認する設計です。このパスは提供された既存実装ではありません。フロント自身の正常性を調べず、バックだけを検査する形へ置き換えないでください。", "### CloudWatch Agent専用プローブ", "`/opt/health/cwagent-process-check`はAWS標準コマンドではありません。現在動いているプロセス確認コマンドを保持するか、第19章冒頭の契約に従う小さな静的プローブを自作・同梱します。この資料にはビルド済みバイナリは含めていません。", "## 20. 読み取り確認コマンド", "Windows PowerShell用。識別子を置き換えて読み取る例であり、資料作成時には実行していません。", "```powershell\n"+d.READ_ONLY_POWERSHELL+"\n```", "## 21. 秒数試算の入力一覧", "Excelの同名シートの太枠入力を変更できます。初期値と区分は以下のとおりです。", md_table(["項目","値","単位","内訳・意味","区分"], [[label,value,unit,desc,kind] for _,label,value,unit,desc,kind in d.INPUTS])]
    chunks += ["## 22. P1の時間軸と300秒・360秒", "これはt0を最初のコンテナ開始とした計画図です。ECS graceの実際の開始点は別途観測してください。", "```text\nt=  0   ADOT・フロント・CWが開始。ALBは登録条件が整えば検査する。\nt= 30   ADOTの応答準備（仮予算）。\nt= 35   CWプロセス確認のHEALTHY検出予算。\nt= 38   ADOTのHEALTHY検出予算 → バック開始。\nt=160   フロント自身の準備予算完了。バックはまだ準備中。\nt=218   バックAPI準備予算完了。フロントの複合readinessも成立。\nt=233   バック・フロントのECS HEALTHY検出予算。\nt=243   ALB healthyの検出予算（回復2回を含む）。\nt=263   登録・ECS反映の通常予算を含む完了点。\nt=300   現在のgrace候補。通常点263から37秒ある。\nt=323   追加予備30+20+10=60秒を全て足した必要予算。\nt=360   提案grace。必要予算323から端数余裕37秒。\n```", "**P4の注意**：制約を無視するとバックHEALTHY226→フロント開始226→複合API386という長い直列になる計算ですが、実際にはバック自身188秒の正常化予算が120秒上限を超えます。後半の時刻が実行される前提で『grace600なら解決』とはいえません。", "## 23. 公式出典と確認範囲"]
    for sid,(title,url,note) in d.SOURCES.items():
        chunks.append(f"- **{sid}** [{title}]({url}) — {note}。確認日：{d.CHECKED}。")
    chunks += ["## 24. 検証と残る事項",md_table(["項目","実施内容・範囲","制約・代替確認","区分"],VERIFY_ROWS)]
    MD.write_text("\n\n".join(chunks)+"\n",encoding="utf-8",newline="\n")


class Book:
    def __init__(self):
        self.wb=xlsxwriter.Workbook(XLSX, {"strings_to_urls":False,"strings_to_formulas":False})
        self.wb.formats[0].set_font_name(FONT)
        self.wb.formats[0].set_font_size(11)
        self.wb.set_properties({"title":"ECS Fargate・ALB 起動とヘルスチェックの詳細設計","subject":"startPeriod / dependsOn / healthCheckGracePeriodSeconds","author":"Codex","comments":"仮定と実測を分けた設計検討資料。AWS環境は未変更。"})
        self.wb.set_calc_mode("auto")
        self.formats={}
        self.sheets=[]
        self.input_cells={}
        self.output_cells={}

    def fmt(self,kind="body",alternate=False):
        key=(kind,alternate)
        if key in self.formats:
            return self.formats[key]
        base=dict(font_name=FONT,font_size=11,font_color="#242424",valign="top",text_wrap=True)
        if kind=="title":
            base.update(font_size=20,bold=True,bg_color="#262626",font_color="#FFFFFF",valign="vcenter")
        elif kind=="header":
            base.update(bold=True,bg_color="#484848",font_color="#FFFFFF",valign="vcenter",border=1,border_color="#808080")
        elif kind=="sub":
            base.update(bold=True,font_size=12,bg_color="#DEDEDE",top=1,bottom=1,border_color="#999999")
        elif kind=="intro":
            base.update(font_size=11,bg_color="#F2F2F2")
        elif kind=="nav":
            base.update(font_size=10,underline=True,font_color="#444444")
        else:
            base.update(border=1,border_color="#D1D1D1",bg_color="#F5F5F5" if alternate else "#FFFFFF")
            if kind=="ref":
                base.update(font_size=10,underline=True,font_color="#404040")
            if kind=="number":
                base.update(align="center",valign="vcenter",num_format='0" 秒"')
            if kind=="input":
                base.update(bold=True,align="center",border=2,border_color="#555555",bg_color="#FFFFFF",num_format="0")
            if kind=="result":
                base.update(bold=True,bg_color="#E0E0E0",align="center",num_format='0" 秒"')
            if kind=="code":
                base.update(font_size=10,bg_color="#F2F2F2")
            if kind=="strong":
                base.update(bold=True)
        fmt=self.wb.add_format(base)
        self.formats[key]=fmt
        return fmt

    @staticmethod
    def text_height(text, width, size=11):
        px=max(20,width*7-14)
        lines=0
        for para in str(text).split("\n"):
            used=0
            lines+=1
            for char in para:
                length=REGULAR.getlength(char)*(size/11)
                if used+length>px:
                    lines+=1
                    used=0
                used+=length
        return min(390,max(25,lines*17+12))

    def init(self,name,title,intro,widths,headers=None):
        ws=self.wb.add_worksheet(name)
        self.sheets.append((name,title))
        ws.hide_gridlines(2)
        ws.set_zoom(80)
        ws.set_tab_color("#505050")
        for c,width in enumerate(widths):
            ws.set_column(c,c,width,self.fmt())
        n=len(widths)
        ws.merge_range(0,0,0,n-1,title,self.fmt("title"))
        ws.set_row(0,43)
        ws.write_url(1,0,"internal:'00_ガイド'!A1",self.fmt("nav"),"目次")
        if n==2:
            ws.write_string(1,1,f"確認日 {d.CHECKED} ｜ 秒数は設計予算 ｜ 実環境で要検証",self.fmt("nav"))
        elif n>2:
            ws.merge_range(1,1,1,n-1,f"確認日 {d.CHECKED} ｜ 秒数は設計予算 ｜ 実環境で要検証",self.fmt("nav"))
        ws.set_row(1,24)
        ws.merge_range(2,0,2,n-1,intro,self.fmt("intro"))
        ws.set_row(2,max(52,self.text_height(intro,sum(widths))))
        ws.set_row(3,10)
        if headers:
            for c,h in enumerate(headers):
                ws.write(4,c,h,self.fmt("header"))
            ws.set_row(4,max(32,max(self.text_height(h,w) for h,w in zip(headers,widths))))
        ws.freeze_panes(5,1)
        ws.set_landscape()
        ws.set_paper(8)  # A3: wide comparison tables remain readable when printed.
        ws.fit_to_pages(1,0)
        ws.set_margins(0.3,0.3,0.4,0.4)
        ws.repeat_rows(0,4)
        ws.set_header('&L&"Meiryo UI,Regular"&9ECS Fargate / ALB  起動設計&R&"Meiryo UI,Regular"&9'+d.CHECKED)
        ws.set_footer('&L&"Meiryo UI,Regular"&8'+name+'&R&"Meiryo UI,Regular"&8&P / &N')
        return ws

    def data(self,ws,rows,widths,start=5,refs=True):
        for ri,values in enumerate(rows,start):
            heights=[]
            for ci,value in enumerate(values):
                alternate=(ri-start)%2==1
                kind="body"
                if ci==0:
                    kind="strong"
                if isinstance(value,(int,float)):
                    fmt=self.fmt("body",alternate)
                    ws.write_number(ri,ci,value,fmt)
                elif refs and ci==len(values)-1 and re.search(r"S\d{2}",str(value)):
                    sid=re.search(r"S\d{2}",value).group()
                    sourcerow=6+list(d.SOURCES).index(sid)
                    ws.write_url(ri,ci,f"internal:'23_出典'!A{sourcerow}",self.fmt("ref",alternate),str(value))
                else:
                    ws.write_string(ri,ci,str(value),self.fmt(kind,alternate))
                heights.append(self.text_height(value,widths[ci]))
            ws.set_row(ri,max(heights))
        last=start+len(rows)-1
        ws.print_area(0,0,max(4,last),len(widths)-1)
        return last+2

    def sections(self):
        for sec in d.SECTIONS:
            ws=self.init(sec["sheet"],sec["title"],sec["intro"],sec["widths"],sec["headers"])
            self.data(ws,sec["rows"],sec["widths"])
            ws.autofilter(4,0,4+len(sec["rows"]),len(sec["headers"])-1)

    def code_block(self,ws,row,title,code,widths):
        ws.merge_range(row,0,row,1,title,self.fmt("sub"))
        ws.set_row(row,30)
        for count,line in enumerate(code.splitlines(),1):
            rr=row+count
            ws.write_number(rr,0,count,self.fmt("body"))
            ws.write_string(rr,1,line,self.fmt("code"))
            ws.set_row(rr,self.text_height(line,widths[1],10))
        return row+len(code.splitlines())+3

    def config(self):
        widths=[15,155]
        ws=self.init("19_設定例","設定例：既存定義へ併合する断片","完全な配備定義ではありません。image・CPU/メモリ・IAM・ネットワーク等は省略。/readyzと自作プローブの実装・同梱が前提。P4の不成立JSONは掲載しません。",widths,["項目 / 行","説明・コード（Meiryo UI）"])
        row=5
        for label,explain,caution,refs in d.CONFIG_NOTES:
            row=self.data(ws,[[label,explain+"\n"+caution+"\n根拠："+refs]],widths,row,False)
        # The complete P1 appears first; all alternatives follow for direct comparison.
        ordering=[d.PATTERNS[i] for i in [1,0,2,3,5,6]]
        for p in ordering:
            row=self.code_block(ws,row,f"{p['id']} {p['name']} ｜ ECS猶予 {p['grace']}秒",json.dumps(d.task_fragment(p),ensure_ascii=False,indent=2),widths)
        row=self.code_block(ws,row,"P1 ECSサービス（ECSローリング更新の設定断片）",json.dumps(d.SERVICE_FRAGMENT,indent=2),widths)
        row=self.code_block(ws,row,"ALBターゲットグループ（フロントHTTP8080の仮定）",json.dumps(d.ALB_FRAGMENT,indent=2),widths)
        row=self.code_block(ws,row,"ADOT health extension（既存Collector設定へ併合）",d.ADOT_CONFIG,widths)
        row=self.code_block(ws,row,"Linuxバック用プローブ例：事前同梱・CA設定が必要",d.BACKEND_SCRIPT,widths)
        row=self.code_block(ws,row,"Linuxフロント用プローブ例：/readyzは複合判定を実装する",d.FRONTEND_SCRIPT,widths)
        ws.print_area(0,0,row,1)
        ws2=self.init("20_確認コマンド","読み取り確認コマンド：PowerShell","資料作成時には実行していません。AWS CLIを利用できる環境で、対象識別子を置き換えて確認してください。外部設定を変更するコマンドは含めていません。",widths,["行","PowerShellコマンド"])
        end=self.code_block(ws2,5,"ECSとALBの現物設定・状態を確認する",d.READ_ONLY_POWERSHELL,widths)
        ws2.print_area(0,0,end,1)

    def calculator(self):
        widths=[60,18,23,75]
        ws=self.init("21_秒数試算","P1：編集可能な秒数試算","太枠の数値は入力。灰色は計算結果。初期値は設計例で、実環境の保証値ではありません。比較表は固定の初期条件、ここはP1の再計算用です。",widths,["項目","値（秒／回）","区分","内訳・使い方"])
        values={key:value for key,_,value,*_ in d.INPUTS}
        for rr,(key,label,value,unit,desc,kind) in enumerate(d.INPUTS,5):
            ws.write(rr,0,label,self.fmt("body",rr%2==0))
            ws.write_number(rr,1,value,self.fmt("input"))
            ws.write(rr,2,kind+" / "+unit,self.fmt("body",rr%2==0))
            ws.write(rr,3,desc,self.fmt("body",rr%2==0))
            ws.set_row(rr,max(self.text_height(label,widths[0]),self.text_height(desc,widths[3]),32))
            self.input_cells[key]=xl_rowcol_to_cell(rr,1,True,True)
            low,high=0,3600
            if "interval" in key: low,high=5,300
            if key in ["a_timeout","b_timeout","f_timeout","c_timeout"]: low,high=2,60
            if key=="alb_timeout": low,high=2,120
            if key=="alb_healthy": low,high=2,10
            if key in ["a_start_timeout","b_start_timeout"]: low,high=2,120
            if key=="grace": low,high=0,2147483647
            ws.data_validation(rr,1,rr,1,{"validate":"integer","criteria":"between","minimum":low,"maximum":high,"input_title":"試算入力","input_message":f"{low}～{high}の整数。未実測値は仮定です。","error_title":"入力値を確認","error_message":f"{low}～{high}の整数を入力してください。","error_type":"stop"})
        row=7+len(d.INPUTS)
        ws.merge_range(row,0,row,3,"計算結果：初期値は第6章と一致",self.fmt("sub"))
        ws.set_row(row,30)
        row+=1
        ic=self.input_cells
        oc=self.output_cells
        m=d.calculate(d.PATTERNS[1])

        def add(key,label,formula,cached,explanation):
            nonlocal row
            ws.write(row,0,label,self.fmt("body"))
            fmt=self.fmt("result") if isinstance(cached,(int,float)) else self.fmt("strong")
            ws.write_formula(row,1,formula,fmt,cached)
            ws.write(row,2,"数式 / 自動計算",self.fmt("body"))
            ws.write(row,3,explanation,self.fmt("body"))
            ws.set_row(row,max(43,self.text_height(explanation,widths[3])))
            oc[key]=xl_rowcol_to_cell(row,1,True,True)
            row+=1

        def sum_input(*keys): return "="+"+".join(ic[k] for k in keys)
        add("a_ready","ADOT 応答準備",sum_input("a_process","a_config","a_receiver","a_publish"),30,"5+10+10+5=30。全て仮予算。")
        add("a_q","ADOT 検出予算",sum_input("a_interval","a_timeout"),8,"5+3=8。厳密上限ではない検出予算。")
        add("a_h","ADOT HEALTHY／バック開始",f"={oc['a_ready']}+{oc['a_q']}",38,"30+8=38。P1のバック開始の計画時刻。")
        add("b_jboss","バック JBoss区間（2倍方針）",sum_input("b_max","b_var"),160,"80+80=160。ユーザーの予備を一度だけ足す。")
        add("b_duration","バック自身のAPI準備",f"={oc['b_jboss']}+{ic['b_pre']}+{ic['b_post']}",180,"160+10+10=180。ADOTを待つ時間は含めない。")
        add("b_q","バック 検出予算",sum_input("b_interval","b_timeout"),15,"10+5=15。")
        add("b_local","バック自身の起動からHEALTHY",f"={oc['b_duration']}+{oc['b_q']}",195,"180+15=195。バックstartPeriodの根拠。")
        add("b_ready","バックAPI準備のt0基準時刻",f"={oc['a_h']}+{oc['b_duration']}",218,"38+180=218。バックHEALTHYの前からAPIは応答可能。")
        add("b_h","バックHEALTHYのt0基準時刻",f"={oc['b_ready']}+{oc['b_q']}",233,"218+15=233。")
        add("f_jboss","フロント JBoss区間（2倍方針）",sum_input("f_max","f_var"),140,"70+70=140。")
        add("f_own","フロント自身の準備",f"={oc['f_jboss']}+{ic['f_pre']}+{ic['f_post']}",160,"140+10+10=160。P1ではt0に起動。")
        add("f_wait","並列でも残るバック待ち",f"=MAX(0,{oc['b_ready']}-{oc['f_own']})",58,"MAX(0,218-160)=58。重なる作業は重複加算しない。")
        add("endpoint","複合readinessの準備時刻",f"=MAX({oc['b_ready']},{oc['f_own']})",218,"自分とバックの遅い方。")
        add("f_q","フロント 検出予算",sum_input("f_interval","f_timeout"),15,"10+5=15。")
        add("f_h","フロントHEALTHY",f"={oc['endpoint']}+{oc['f_q']}",233,"218+15=233。")
        add("c_h","CW Agent HEALTHY",sum_input("c_process","c_config","c_visible","c_interval","c_timeout"),35,"5+10+5+10+5=35。並列なので全体へ足さない。")
        add("task","4コンテナがそろう時刻",f"=MAX({oc['a_h']},{oc['b_h']},{oc['f_h']},{oc['c_h']})",233,"4つのHEALTHY時刻の最大値。")
        add("alb_q","ALB 回復検出予算",f"={ic['alb_interval']}*{ic['alb_healthy']}+{ic['alb_timeout']}",25,"10×2+5=25。新規初回1成功だけの場合とは区別。")
        add("alb","ALB healthyの計画時刻",f"={oc['endpoint']}+{oc['alb_q']}",243,"218+25=243。ECS F HEALTHYからさらに待つ計算ではない。")
        add("normal","通常の配備正常化予算",f"=MAX({oc['task']},{oc['alb']})+{ic['registration']}+{ic['ecs_report']}",263,"MAX(233,243)+10+10=263。通常の反映20秒込み。")
        add("spare_probe","追加予備① ALB一時失敗",f"={ic['extra_failures']}*{ic['alb_interval']}",30,"3×10=30。追加周期の設計枠。")
        add("spare","追加予備 合計",f"={oc['spare_probe']}+{ic['extra_control']}+{ic['observation']}",60,"一時失敗30＋制御面超過20＋観測10=60。")
        add("required","必要grace予算（端数処理前）",f"=MAX(0,{oc['normal']}+{oc['spare']}-{ic['grace_origin']})",323,"263+60-0=323。実際の猶予開始差を入力して再評価。")
        add("suggested","60秒単位に切り上げた候補",f"=CEILING({oc['required']},60)",360,"323→360。端数余裕37秒。")
        add("margin","入力graceに対する余裕",f"={ic['grace']}-{oc['required']}",37,"360-323=37。負値ならこの予算では不足。")
        add("g300","grace300を選んだ場合の余裕",f"=300-{oc['required']}",-23,"300-323=-23。通常点263には間に合う例だが、追加予備込みでは不足。")
        add("a_gate","ADOT依存先期限の余裕",f"={ic['a_start_timeout']}-{oc['a_h']}",82,"120-38=82。0以下は依存条件の成立を見込めない。")
        add("b_gate","バックHEALTHY直列化の期限余裕",f"={ic['b_start_timeout']}-{oc['b_local']}",-75,"P1の10/5検査では120-195=-75。P4の速い5/3でも120-188=-68。")
        add("a_sp","ADOT startPeriod45の余裕",f"=45-{oc['a_h']}",7,"候補45と初回HEALTHY予算38の差。")
        add("b_sp","バックstartPeriod210の余裕",f"=210-{oc['b_local']}",15,"候補210と自分のHEALTHY予算195の差。")
        add("f_sp","フロントstartPeriod240の余裕",f"=240-{oc['f_h']}",7,"P1ではフロント開始=t0。候補240と233の差。")
        add("c_sp","CW startPeriod60の余裕",f"=60-{oc['c_h']}",25,"候補60と35の差。")
        add("decision","P1の予算評価",f'=IF(AND({oc["margin"]}>=0,{oc["a_gate"]}>0,{oc["a_sp"]}>=0,{oc["b_sp"]}>=0,{oc["f_sp"]}>=0,{oc["c_sp"]}>=0),"予算内（実測要）","要再設計")',"予算内（実測要）","grace・ADOT依存・4つのstartPeriodをまとめて確認。トレース配送や実環境動作は別検証。")
        ws.conditional_format(5,1,row-1,1,{"type":"cell","criteria":"<","value":0,"format":self.wb.add_format({"font_name":FONT,"font_color":"#FFFFFF","bg_color":"#404040","bold":True})})
        ws.print_area(0,0,row-1,3)
        return m

    def timeline(self):
        widths=[25,20,20,20,22,58]
        ws=self.init("22_時間軸図","起動の時間軸：並列と直列を比べる","棒は各処理の開始から準備・検出までの計画区間。実時間の予測値ではありません。P4は依存上限違反のためグラフに含めません。",widths,["表示","開始（秒）","区間（秒）","終了（秒）","区分","説明"])
        p1=d.calculate(d.PATTERNS[1]); p3=d.calculate(d.PATTERNS[3])
        graph_rows=[
            ["P1 ADOT",0,38,38,"仮定＋検出","準備30と検出8。終了でバックを開始。"],
            ["P1 CW Agent",0,35,35,"仮定＋検出","別枝。全体には足し算しない。"],
            ["P1 バック",38,195,233,"起動＋検出","API自体は218で準備可能という予算。"],
            ["P1 フロント自身",0,160,160,"自身の起動","バックAPIを待つ前の自分の準備。"],
            ["P1 Fの残待ち・検出",160,73,233,"待ち58＋検出15","フロントとバックの準備を重ねる。"],
            ["P1 ALB検出",218,25,243,"独立検査","ECSの233まで待ってから検査するのではない。"],
            ["P1 通常反映",243,20,263,"制御面予算","登録10＋ECS反映10。"],
            ["P1 追加予備",263,60,323,"設計上の予備","一時失敗30＋制御超過20＋観測10。"],
            ["P1 切上げ余裕",323,37,360,"端数","猶予360の根拠。"],
            ["P3 ADOT",0,38,38,"仮定＋検出","実測ベースの直列例。"],
            ["P3 バック",38,108,146,"起動＋検出","80＋ログ外20＋検出8。120上限まで12。"],
            ["P3 フロント",146,105,251,"起動＋検出","70＋ログ外20＋検出15。"],
            ["P3 ALB検出",236,25,261,"独立検査","フロントAPI準備236から検査する計画。"],
            ["P3 通常反映",261,20,281,"制御面予算","通常予算281。追加60で341。"],
        ]
        # Put the table below two charts; sources are visible and all values are inspectable.
        table_start=55
        for c,h in enumerate(["表示","開始（秒）","区間（秒）","終了（秒）","区分","説明"]):
            ws.write(table_start-1,c,h,self.fmt("header"))
        self.data(ws,graph_rows,widths,table_start,False)
        for pos,start,end,title in [(5,0,8,"P1：2倍見積もりを含む並列起動の予算"),(30,9,13,"P3：実測上限だけを保護する直列起動の予算")]:
            chart=self.wb.add_chart({"type":"bar","subtype":"stacked"})
            chart.add_series({"name":"開始まで","categories":[ws.name,table_start+start,0,table_start+end,0],"values":[ws.name,table_start+start,1,table_start+end,1],"fill":{"none":True},"border":{"none":True}})
            chart.add_series({"name":"処理・検出の予算（秒）","categories":[ws.name,table_start+start,0,table_start+end,0],"values":[ws.name,table_start+start,2,table_start+end,2],"fill":{"color":"#777777"},"border":{"color":"#454545"},"data_labels":{"value":True,"position":"center","font":{"name":FONT,"size":10,"color":"#FFFFFF"}}})
            chart.set_title({"name":title,"name_font":{"name":FONT,"size":14,"color":"#202020"}})
            chart.set_x_axis({"name":"t0からの計画秒数（猶予開始とは区別）","min":0,"max":360,"major_unit":60,"num_font":{"name":FONT,"size":10},"name_font":{"name":FONT,"size":10},"major_gridlines":{"visible":True,"line":{"color":"#D0D0D0"}}})
            chart.set_y_axis({"reverse":True,"num_font":{"name":FONT,"size":10}})
            chart.set_legend({"none":True})
            chart.set_chartarea({"border":{"color":"#AAAAAA"},"fill":{"color":"#FFFFFF"}})
            chart.set_plotarea({"border":{"none":True},"fill":{"color":"#FFFFFF"}})
            chart.set_size({"width":1110,"height":440})
            ws.insert_chart(pos,0,chart,{"x_offset":4,"y_offset":4,"object_position":1})
        for r in range(5,54): ws.set_row(r,14)
        ws.freeze_panes(5,0)
        ws.print_area(0,0,table_start+len(graph_rows),5)

    def sources(self):
        widths=[9,36,80,62,17]
        ws=self.init("23_出典","公式出典：API・製品資料・公式実装","各章のS番号はこの一覧へ移動します。URLは公式資料または公式ソース。ADOT/CW実装は確認したコミットに固定。上流mainの文書は将来変更されます。",widths,["ID","資料","URL（クリック可能）","確認した内容","確認日"])
        for r,(sid,(title,url,note)) in enumerate(d.SOURCES.items(),5):
            alt=r%2==0
            ws.write(r,0,sid,self.fmt("strong",alt))
            ws.write(r,1,title,self.fmt("body",alt))
            ws.write_url(r,2,url,self.fmt("ref",alt),url)
            ws.write(r,3,note,self.fmt("body",alt))
            ws.write(r,4,d.CHECKED,self.fmt("body",alt))
            ws.set_row(r,max(self.text_height(title,widths[1]),self.text_height(url,widths[2]),self.text_height(note,widths[3])))
        ws.autofilter(4,0,len(d.SOURCES)+4,4)
        ws.print_area(0,0,len(d.SOURCES)+4,4)

    def guide(self):
        widths=[24,58,55,24]
        ws=self.init("00_ガイド","ECS Fargate / ALB  起動・ヘルスチェック詳細設計","160秒・140秒はJBoss実測最大の2倍見積もり。起動順、ヘルスチェック、猶予を分け、バッファ内訳から具体値を計算する資料です。",widths,["読み順","見る内容","押さえること","移動先"])
        rows=[
            ["最初に","P1：ADOT→バック、フロント並列","startPeriod：A45 / C60 / B210 / F240。ECS猶予360。未実測部分は仮予算。","01_結論と前提"],
            ["仕組みを理解","小学生にも分かるお店の比喩","startPeriodは検査を止めない。graceもALB検査を止めない。","02_やさしい仕組み"],
            ["値域を確認","設定場所・指定可能範囲・既定値","startPeriod上限300、Fargate startTimeout上限120。","03_指定できる値"],
            ["バッファを確認","何秒を何のために足したか","80+80=160を一度だけ加算。並列はMAX。","06_バッファ内訳"],
            ["方式を比較","P0～P6の採否と設定","P4は不成立。grace600でも依存待ち120は伸びない。","07_パターン比較"],
            ["ヘルスを修正","フロント自身とバックの両方を検査","バックだけの200ではフロントの準備を証明できない。","11_ヘルス経路"],
            ["数値を試す","35項目の入力と数式","太枠入力を変更しP1を再計算。固定比較表とは別。","21_秒数試算"],
            ["時間軸を見る","P1・P3のグラフ","処理の重なりと、直列化で足される待ちを確認。","22_時間軸図"],
            ["採用前に","設定断片・実装前提・試験手順","/readyzと専用プローブ、イメージ内コマンドの確認が必要。","19_設定例"],
            ["根拠に戻る","公式資料44件","確認日と出典、実測・仮定・提案の区分を参照。","23_出典"],
        ]
        end=self.data(ws,rows,widths,5,False)
        for r,values in enumerate(rows,5):
            ws.write_url(r,3,f"internal:'{values[3]}'!A1",self.fmt("ref",r%2==0),values[3])
        ws.merge_range(end,0,end,3,"全シート索引",self.fmt("sub")); ws.set_row(end,30)
        self.guide_sheet=ws
        self.guide_index_row=end+1
        self.guide_widths=widths
        ws.activate()
        ws.set_first_sheet()

    def finish_guide(self):
        rows=[]
        for name,title in self.sheets:
            if name!="00_ガイド": rows.append([name,title,"内容確認・比較に利用",name])
        self.data(self.guide_sheet,rows,self.guide_widths,self.guide_index_row,False)
        for r,row in enumerate(rows,self.guide_index_row):
            self.guide_sheet.write_url(r,3,f"internal:'{row[3]}'!A1",self.fmt("ref"),"このシートへ")

    def build(self):
        self.guide()
        self.sections()
        self.config()
        self.calculator()
        self.timeline()
        self.sources()
        widths=[25,65,62,18]
        ws=self.init("24_検証と制約","検証範囲と未確定事項","公式仕様の調査と成果物の検証を実施。実AWS・JBoss・Collectorの動作試験は、採用前に別途必要です。",widths,["項目","確認内容","制約と残る作業","区分"])
        self.data(ws,VERIFY_ROWS,widths,refs=False)
        self.finish_guide()
        self.wb.close()
        manifest={"checked":d.CHECKED,"xlsx":XLSX.name,"md":MD.name,"sheets":[x[0] for x in self.sheets],"input_cells":self.input_cells,"output_cells":self.output_cells,"patterns":{p['id']:d.calculate(p) for p in d.PATTERNS}}
        (OUT/"calculation_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    write_markdown()
    Book().build()
    print(json.dumps({"xlsx":str(XLSX),"markdown":str(MD),"sources":len(d.SOURCES),"patterns":len(d.PATTERNS)},ensure_ascii=False))
