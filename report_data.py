"""Content and planning assumptions for the ECS health-check design report."""

CHECKED = "2026-10-12"
SOURCES = {
    "S01": ("ECS HealthCheck API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_HealthCheck.html", "startPeriod・interval・timeout・retriesの仕様と範囲"),
    "S02": ("ECS コンテナヘルスチェック", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/healthcheck.html", "コンテナとタスクの健康状態、チェックの実行場所"),
    "S03": ("ECS ContainerDependency API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDependency.html", "START / COMPLETE / SUCCESS / HEALTHY、起動時評価"),
    "S04": ("ECS ContainerDefinition API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html", "startTimeoutの設定先と2～120秒、essential、stopTimeout"),
    "S05": ("ECS サービス定義パラメータ", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_definition_parameters.html", "サービス猶予の意味、最大値、更新時の扱い"),
    "S06": ("ECS CreateService API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateService.html", "猶予が無視する失敗、desiredCount超過時の例外"),
    "S07": ("ALB ターゲットヘルスチェック", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html", "チェック条件・値域、fail-open、理由コード"),
    "S08": ("ECS ロードバランサーヘルスチェック最適化", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-healthcheck.html", "新規登録時1回成功とunhealthyからの回復の違い"),
    "S09": ("ELB CreateTargetGroup API", "https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_CreateTargetGroup.html", "ALBの間隔・パス・ポート等のAPI仕様"),
    "S10": ("ALB ターゲットグループ属性", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html", "登録解除待ち、slow start、トラフィック制御"),
    "S11": ("ELB TargetGroupAttribute API", "https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_TargetGroupAttribute.html", "deregistration delayとslow startの値域"),
    "S12": ("Fargate タスクネットワーク", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html", "同一タスクのlocalhost共有、ENI"),
    "S13": ("ECS でのALB利用", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/alb.html", "awsvpcでターゲットタイプipを使う"),
    "S14": ("ECS DeploymentConfiguration API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeploymentConfiguration.html", "更新時に数える正常タスク、100%/200%の意味"),
    "S15": ("ECS Task API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Task.html", "startedAtとpull時刻、停止理由"),
    "S16": ("ECS タスクライフサイクル", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-lifecycle-explanation.html", "ACTIVATING・RUNNINGなどの状態"),
    "S17": ("ECS メタデータV4", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint-v4-response.html", "コンテナごとのStartedAt等"),
    "S18": ("ADOT healthcheck実装", "https://github.com/aws-observability/aws-otel-collector/blob/7579e0913cc764588c356a61616d6bca021f6b8d/cmd/healthcheck/main.go", "127.0.0.1:13133のHTTP 200を調べる実装"),
    "S19": ("ADOT Dockerfile", "https://github.com/aws-observability/aws-otel-collector/blob/7579e0913cc764588c356a61616d6bca021f6b8d/cmd/awscollector/Dockerfile", "scratchイメージと/healthcheckの同梱"),
    "S20": ("OpenTelemetry Health Check Extension", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/extension/healthcheckextension/README.md", "endpoint・path、pipelineチェックの制約"),
    "S21": ("OpenTelemetry Collector設定", "https://opentelemetry.io/docs/collector/configuration/", "health_checkの定義とservice.extensionsによる有効化"),
    "S22": ("OpenTelemetry Collectorの耐障害性", "https://opentelemetry.io/docs/collector/resiliency/", "送信キュー・再試行・永続化、ロスの限界"),
    "S23": ("CloudWatch Agent Dockerfile", "https://github.com/aws/amazon-cloudwatch-agent/blob/e175d648886dd5c79b36bc894a6033ab94049cdd/amazon-cloudwatch-container-insights/cloudwatch-agent-dockerfile/Dockerfile", "scratch、シェルやctlコマンドを前提にできない"),
    "S24": ("CloudWatch procstat", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-procstat-process-metrics.html", "procstatプラグインはECS Fargate非対応。自分のプロセス確認とは別"),
    "S25": ("ECS Fargate タスク定義", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html", "各パラメータ、依存先タイムアウト、PID名前空間"),
    "S26": ("Terraform depends_on", "https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on", "リソース依存とコンテナ起動依存の区別"),
    "S27": ("CloudFormation HealthCheck", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-ecs-taskdefinition-healthcheck.html", "CloudFormationのプロパティ名と範囲"),
    "S28": ("CloudFormation ContainerDependency", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-ecs-taskdefinition-containerdependency.html", "ContainerName・Conditionという表記"),
    "S29": ("Dockerfile HEALTHCHECK", "https://docs.docker.com/reference/dockerfile/#healthcheck", "実行と正常判定、Docker独自start-intervalとの区別"),
    "S30": ("curl マニュアル", "https://curl.se/docs/manpage.html", "--write-out・--cacert・--resolve・--max-time"),
    "S31": ("JBoss EAP 8 設定ガイド", "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.0/html-single/configuration_guide/index", "起動と要求受付の関係。利用EAPバージョンは未確認"),
    "S32": ("JBoss EAP XP 5 のHealth", "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.0/html-single/using_jboss_eap_xp_5.0/index", "server / boot / deployment別の確認。導入有無は別途確認"),
    "S33": ("2017 ECS猶予導入", "https://aws.amazon.com/about-aws/whats-new/2017/12/amazon-ecs-adds-elb-health-check-grace-period/", "2017-12-27の発表"),
    "S34": ("2018 ECSコンテナHealth導入", "https://aws.amazon.com/about-aws/whats-new/2018/03/amazon-ecs-supports-container-health-checks-and-task-health-mana/", "2018-03-08の発表"),
    "S35": ("2019 ECS依存関係強化", "https://aws.amazon.com/about-aws/whats-new/2019/03/amazon-ecs-introduces-enhanced-container-dependency-management/", "2019-03-07の発表"),
    "S36": ("ALBの履歴", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/doc-history.html", "2016-08-11 ALB、2018-03-24 slow start"),
    "S37": ("Fargate発表", "https://aws.amazon.com/about-aws/whats-new/2017/11/introducing-aws-fargate-a-technology-to-run-containers-without-managing-infrastructure/", "2017-11-29の発表"),
    "S38": ("CloudWatch統合Agent発表", "https://aws.amazon.com/about-aws/whats-new/2017/12/amazon-cloudwatch-introduces-a-new-cloudwatch-agent-with-aws-systems-manager-integration-for-unified-metrics-and-logs-collection/", "2017-12-14の発表"),
    "S39": ("ADOT tracing GA", "https://aws.amazon.com/blogs/opensource/aws-distro-for-opentelemetry-is-now-ga-for-tracing/", "2020-10 preview、2021-09-29 tracing GA"),
    "S40": ("ECS コンテナ再起動ポリシー", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-restart-policy.html", "コンテナ終了時にタスク全体を交換しない例外"),
    "S41": ("Spring Boot Health endpoints", "https://docs.spring.io/spring-boot/reference/actuator/endpoints.html", "livenessへの外部依存混入とreadinessの設計上の注意"),
    "S42": ("Terraform AWS provider ECS Service", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/ecs_service.html.markdown", "health_check_grace_period_secondsのHCL名"),
    "S43": ("Terraform AWS provider ECS Task Definition", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/ecs_task_definition.html.markdown", "container_definitionsへJSONを指定する"),
    "S44": ("CloudFormation ECS Service", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-service.html", "HealthCheckGracePeriodSecondsの表記"),
}

# User supplied measurements are distinct from the assumptions below.
INPUTS = [
    ("b_max", "バック：実測最大（JBoss開始→デプロイ完了）", 80, "秒", "ユーザー実測20～80秒の最大", "実測"),
    ("f_max", "フロント：実測最大（同上）", 70, "秒", "ユーザー実測15～70秒の最大", "実測"),
    ("b_var", "バック：起動変動の予備", 80, "秒", "最大値を2倍にするユーザー方針：80秒を追加", "ユーザー見積もり"),
    ("f_var", "フロント：起動変動の予備", 70, "秒", "最大値を2倍にするユーザー方針：70秒を追加", "ユーザー見積もり"),
    ("b_pre", "バック：コンテナ開始→JBoss開始ログ", 10, "秒", "entrypoint、設定展開など。未実測の仮予算", "仮定"),
    ("b_post", "バック：完了ログ→APIの安定200", 10, "秒", "業務初期化・要求受付の差分。未実測", "仮定"),
    ("f_pre", "フロント：コンテナ開始→JBoss開始ログ", 10, "秒", "entrypoint、設定展開など。未実測", "仮定"),
    ("f_post", "フロント：完了ログ→自分のHTTP受付", 10, "秒", "自分の経路の準備。バック待ちはここに含めない", "仮定"),
    ("a_process", "ADOT：プロセスの開始準備", 5, "秒", "コンテナ開始から実行準備まで", "仮定"),
    ("a_config", "ADOT：設定読込・検証", 10, "秒", "設定展開・pipeline生成の予算", "仮定"),
    ("a_receiver", "ADOT：receiver初期化・listen", 10, "秒", "OTLPなど利用するreceiverの初期化予算", "仮定"),
    ("a_publish", "ADOT：13133の応答準備", 5, "秒", "HTTP health応答までの追加予算。外部配送成功は含めない", "仮定"),
    ("c_process", "CW：起動準備", 5, "秒", "CloudWatch Agentの起動準備", "仮定"),
    ("c_config", "CW：設定処理", 10, "秒", "設定を読んで本体を起動する予算", "仮定"),
    ("c_visible", "CW：対象プロセス確認まで", 5, "秒", "対象プロセスが確認可能になるまでの予算", "仮定"),
    ("a_interval", "ADOT interval", 5, "秒", "コンテナヘルスチェック間隔", "設定"),
    ("a_timeout", "ADOT timeout", 3, "秒", "1回の実行制限", "設定"),
    ("b_interval", "バック interval", 10, "秒", "P1の設定。P3/P4は5秒", "設定"),
    ("b_timeout", "バック timeout", 5, "秒", "P1の設定。P3/P4は3秒", "設定"),
    ("f_interval", "フロント interval", 10, "秒", "フロント自身＋バックを確認", "設定"),
    ("f_timeout", "フロント timeout", 5, "秒", "1回の実行制限", "設定"),
    ("c_interval", "CW interval", 10, "秒", "対象プロセスの確認間隔", "設定"),
    ("c_timeout", "CW timeout", 5, "秒", "1回の実行制限", "設定"),
    ("alb_interval", "ALB interval", 10, "秒", "ターゲットグループのチェック間隔", "設定"),
    ("alb_timeout", "ALB timeout", 5, "秒", "1回の応答予算", "設定"),
    ("alb_healthy", "ALB healthy threshold", 2, "回", "unhealthyからの回復を想定", "設定"),
    ("registration", "ALB登録・反映の遅れ予算", 10, "秒", "重ならない側に保守的に加算。API保証値ではない", "仮定"),
    ("ecs_report", "ECSへの正常状態反映予算", 10, "秒", "制御面の通知・評価待ち。API保証値ではない", "仮定"),
    ("extra_failures", "追加予備：ALBの一時失敗", 3, "回", "正常化後の3回分の追加チェック周期を予算化", "方針"),
    ("extra_control", "追加予備：制御面遅延の延長枠", 20, "秒", "通常の反映予算20秒とは別の超過分。未実測", "方針"),
    ("observation", "追加予備：時刻観測の不確かさ", 10, "秒", "ログ採取・観測間隔等。実測方法確立後に見直す", "方針"),
    ("grace_origin", "猶予開始時刻－図のt0", 0, "秒", "0は保守的仮定。実運用はECSのtask startedAt等で確認", "仮定"),
    ("grace", "P1 ECS service grace", 360, "秒", "323秒を60秒単位で切り上げる初期案", "提案"),
    ("a_start_timeout", "ADOT startTimeout", 120, "秒", "依存先ADOTに置く。Fargate上限", "設定"),
    ("b_start_timeout", "バック startTimeout（HEALTHY依存用）", 120, "秒", "P3/P4で依存先バックに置く。P1では不要", "設定"),
]

PATTERNS = [
    dict(id="P0", name="現在の並列構成を評価", mode="parallel", use_buffer=True, a_sp=45,b_sp=210,f_sp=210,c_sp=60,b_i=10,b_t=5,grace=300, b_dep="なし",f_dep="なし",decision="起動時間は成立例あり。初期トレース要件は別途対策", note="フロントの現行チェックがバックだけなら、自分の正常性を追加する。"),
    dict(id="P1", name="推奨：ADOT→バック、フロント並列", mode="hybrid", use_buffer=True,a_sp=45,b_sp=210,f_sp=240,c_sp=60,b_i=10,b_t=5,grace=360,b_dep="adot / HEALTHY",f_dep="なし",decision="160秒・140秒の見積もりを尊重する初期案",note="バック待ち58秒がフロント自身のstartPeriodにも入る。フロントがバック未起動に耐えること。"),
    dict(id="P2", name="短縮：実測後に余裕を縮小", mode="hybrid", use_buffer=False,a_sp=45,b_sp=120,f_sp=180,c_sp=60,b_i=10,b_t=5,grace=300,b_dep="adot / HEALTHY",f_dep="なし",decision="2倍の起動変動予備を外す条件付き案",note="多数回の観測で採否判断。今すぐP1を置換する推奨ではない。"),
    dict(id="P3", name="直列：実測上限内だけを保護", mode="serial", use_buffer=False,a_sp=45,b_sp=120,f_sp=120,c_sp=60,b_i=5,b_t=3,grace=360,b_dep="adot / HEALTHY",f_dep="backend / HEALTHY",decision="バックの正常化が120秒未満に収まる場合のみ",note="モデルでバック108秒、上限まで12秒。160秒の起動見積もり全体は保護できない。"),
    dict(id="P4", name="不採用：2倍見積もりを直列で待つ", mode="serial", use_buffer=True,a_sp=45,b_sp=210,f_sp=180,c_sp=60,b_i=5,b_t=3,grace=600,b_dep="adot / HEALTHY",f_dep="backend / HEALTHY",decision="不成立：バック188秒＞startTimeout 120秒",note="猶予600秒でも依存先待ちの上限は延びない。計算後半は制限を無視した反実仮想。"),
    dict(id="P5", name="START順序＋アプリ側の待機", mode="start", use_buffer=True,a_sp=45,b_sp=210,f_sp=210,c_sp=60,b_i=10,b_t=5,grace=360,b_dep="adot / HEALTHY",f_dep="backend / START",decision="起動順・停止順を残しつつAPI待ちはアプリが担当",note="STARTはAPI利用可能を保証しない。有限の再試行と複合readinessを実装する。"),
    dict(id="P6", name="両アプリがADOTだけを待つ", mode="siblings", use_buffer=True,a_sp=45,b_sp=210,f_sp=210,c_sp=60,b_i=10,b_t=5,grace=360,b_dep="adot / HEALTHY",f_dep="adot / HEALTHY",decision="フロントも起動直後にトレースを送る場合の候補",note="バックとフロントは兄弟として同時進行。両方の停止後までADOTを残せる。"),
]

SECTIONS = []

def section(sheet, title, intro, rows, headers=None, widths=None):
    SECTIONS.append(dict(sheet=sheet,title=title,intro=intro,rows=rows,
                         headers=headers or ["項目", "動作・説明", "今回の設計への適用", "根拠"],
                         widths=widths or [25,66,52,14]))

section("01_結論と前提", "結論と確認できた前提", "結論：フロントとバックのHEALTHY直列化を外し、利用可否を正しいヘルスチェックで表すP1が第一候補。数値は未実測のサイドカー等を含む設計例であり、本番での保証値ではありません。", [
    ["第一候補 P1", "ADOTがHEALTHYになってからバックを開始。フロントとCloudWatch Agentは独立して開始する。フロントの正常条件は『自分が受付可能 AND バックAPIが利用可能』。", "StartPeriod：ADOT45／CW60／バック210／フロント240秒。サービス猶予360秒。ALB間隔10・timeout5・正常2回・異常3回。", "S01 S03 S04"],
    ["補足を反映済み", "160秒＝バック実測最大80秒＋変動予備80秒。140秒＝フロント実測最大70秒＋変動予備70秒。いずれもJBoss EAP開始ログ→デプロイ完了ログの区間。", "sleepで実際に160秒・140秒待たせている、と解釈しない。過去の最大値×2は見積もり方針であり、将来の最大値やp99ではない。", "ユーザー"],
    ["現在の210秒", "両コンテナのstartPeriod=210秒は、指定可能な0～300秒の範囲内。起動完了を210秒まで待たせる機能ではない。", "80秒で正常応答し、次の検査が成功すれば、210秒より前にHEALTHYになる。短くするだけでデプロイが速くなるわけではない。", "S01 S02"],
    ["300秒の項目は未確認", "本文ではECSサービスのhealthCheckGracePeriodSeconds=300として評価する。ALBの登録解除待ち300秒だった場合、起動保護の効果はない。", "現物の項目名を読み取り確認する。ECSサービス猶予の初期値は0、ALB登録解除待ちの初期値は300秒であり、取り違えやすい。", "S05 S10"],
    ["直列化の本当の制約", "HEALTHY依存では、FargateのstartTimeoutに2～120秒という制約がある。依存先の初回正常化が188秒になる設計例は、この制約を超える。", "バック実測80秒では成功し得る。しかし160秒までを見込む方針と『フロントがバックHEALTHYを待つ』は両立するとはいえない。", "S04 S25"],
    ["バックだけを見る問題", "フロント内でlocalhost:18080を呼んでも、調べている相手はバック。フロントのJBossやHTTP経路が壊れていても、バックが200なら成功し得る。", "フロント自身のreadinessかフロントを通る経路を必ず含める。ALBもフロントのその経路を調べる。", "S12 設計"],
    ["対象と仮定", "ECS Service＋Linux Fargate＋awsvpc＋ALBのHTTP/HTTPSターゲットを対象とする。4コンテナともessential=true、restartPolicyは有効化しない前提。", "コンテナイメージ、EAPバージョン、フロントのポート、TLS証明書、実際のタスク定義は未提供。例の8080と/readyzは提案用の名前。", "前提"],
    ["確認範囲", "作業フォルダーには既存の設定・ソース・Git管理情報がなかった。AWSやアプリの実環境へ接続した確認は行っていない。公式資料を調査し、計算とファイルを検証した。", "設定例は既存定義に併合する検討用断片。新しいイメージやreadinessを実装せず、そのまま本番登録できる完全定義ではない。", "作業記録"],
])

section("02_やさしい仕組み", "お店の開店準備で理解する", "フロント＝注文窓口、バック＝厨房、ADOT＝記録係、CloudWatch Agent＝見回り係、ALB＝案内係、ECS＝店長と考えると、役割の違いが分かります。", [
    ["タスク", "ひとつのお店に4人がいるイメージ。4つのコンテナは別の仕事をするが、同じタスクの中で一緒に動く。", "全部の準備を順番に待てば合計が長くなる。同時に準備できる仕事は重ねる。", "説明用の比喩"],
    ["プロセス開始", "厨房の人がお店に来た状態。まだ火をつけたり材料を出したりしているかもしれない。", "コンテナRUNNINGやdependsOn STARTは、この段階に近い。APIを使えることとは分ける。", "S03 S16"],
    ["readiness", "厨房が『今なら料理を出せる』と言える状態。窓口も『今なら注文を受けて渡せる』状態を調べる。", "JBossのログだけでなく、実際のポートとパスで利用可能を確認する。", "設計 S31"],
    ["startPeriod", "店長が開店準備中の失敗にバツを付けない期間。確認の声掛けは準備中でも続く。できたと答えれば、その時点で合格。", "最初に一度合格すると、その後の連続失敗はstartPeriod中でも数える。固定の待機時間ではない。", "S01"],
    ["interval / timeout", "intervalは『何秒おきに聞くか』。timeoutは『1回聞いて何秒まで返事を待つか』。", "間隔10秒、応答制限5秒なら、準備完了を見つけるまでの設計予算を15秒と置く。ただし実装・伝播を含む厳密な上限ではない。", "S01 設計"],
    ["retries", "何回続けて返事がなければ具合が悪いとするか。成功すれば連続失敗の列は切れる。", "retries=3は合格に3回必要という意味ではない。コンテナは基本的に1回の成功でHEALTHYになる。", "S01 S29"],
    ["サービスの猶予", "店長が、開店直後の検査失敗だけで店を作り直さない期間。案内係はその間も検査する。", "ALBのチェック停止でも、利用者を必ず通さない門でもない。", "S05 S07"],
    ["dependsOn HEALTHY", "『厨房が準備できたと言うまで、窓口の人は自分の準備を始めない』という約束。", "本当に必要な順番だけに使う。厨房の待ち期限と窓口自身の起動猶予は別々。", "S03 S04"],
    ["startTimeout", "『相手の準備をいつまで待つか』という待ち合わせの締め切り。", "Fargateでは設定上限120秒。店長の猶予を600秒にしても、この待ち合わせ期限は伸びない。", "S04"],
    ["なぜ監視が複数あるか", "自分で調べる検査と、外の案内係から入り口を通って調べる検査は、違う故障を見つける。", "コンテナ内部の成功だけでは、ALB→ENI→フロントのネットワークやパスが通るとは限らない。", "S02 S07 S12"],
])

section("03_指定できる値", "設定できる値と設定場所", "単位は特記しない限り秒。APIの許容範囲と、今回選ぶ設計値を区別します。整数で指定する値を小数で入れないでください。", [
    ["コンテナ", "healthCheck.startPeriod", "0～300／既定0（無効）", "P1 A45・C60・B210・F240", "起動時失敗を数えない猶予。各コンテナ自身の起動基準。", "S01"],
    ["コンテナ", "healthCheck.interval", "5～300／既定30", "A5・ほか10", "短いほど検出が速いが、チェック負荷が増える。", "S01"],
    ["コンテナ", "healthCheck.timeout", "2～60／既定5", "A3・ほか5", "1回のコマンドの期限。ALB側のtimeoutとは独立。", "S01"],
    ["コンテナ", "healthCheck.retries", "1～10回／既定3", "全て3", "連続失敗の閾値。初回正常化を3回待つ値ではない。", "S01"],
    ["コンテナ", "healthCheck.command", "文字列配列。CMD または CMD-SHELLで始める", "ADOTはCMD /healthcheck", "終了コード0が成功。shellなしイメージではCMD-SHELLを使えない。", "S01 S19"],
    ["コンテナ", "startTimeout", "Fargate 2～120", "待たれるADOTに120。P3/P4ではバックにも120", "未指定時の値に依存せず明示する。startPeriodとは別物。", "S04"],
    ["コンテナ", "stopTimeout", "Fargate 2～120／既定30", "既存値を維持。必要なら実測で30→60等", "停止シグナル後の終了待ち。起動問題の調整つまみではない。", "S04"],
    ["コンテナ", "essential", "true / false／省略時true", "4コンテナともtrue", "正しい綴りはessential。essentialsではない。", "S04"],
    ["コンテナ", "dependsOn[].condition", "START / COMPLETE / SUCCESS / HEALTHY", "P1 バック→adot HEALTHY", "COMPLETE/SUCCESSはessentialな依存先には使えない。常駐プロセスの完了待ちにしない。", "S03"],
    ["ECSサービス", "healthCheckGracePeriodSeconds", "0～2,147,483,647／既定0", "P1 360。P0/P2 300", "異常ヘルスを理由にした交換の猶予。ALBの検査開始時刻ではない。", "S05 S06"],
    ["ALBターゲット群", "HealthCheckIntervalSeconds", "5～300／ipの場合既定30", "10", "各ターゲットへの検査間隔。300秒にして起動を待たせる設計にしない。", "S09"],
    ["ALBターゲット群", "HealthCheckTimeoutSeconds", "2～120／ipの場合既定5", "5", "無応答を失敗とする期限。300秒は範囲外。", "S07"],
    ["ALBターゲット群", "HealthyThresholdCount", "2～10回／既定5", "2", "unhealthyからhealthyへの回復に必要な連続成功。新規登録初回は別扱い。", "S07 S08"],
    ["ALBターゲット群", "UnhealthyThresholdCount", "2～10回／既定2", "3", "短い一過性障害に少し余裕を持たせる例。検出が遅れるトレードオフ。", "S07"],
    ["ALBターゲット群", "Matcher.HttpCode", "HTTP/1.1, HTTP/2：200～499／既定200", "200のみ", "200-499等に広げると404や認証エラーを成功にするため不適切。", "S07"],
    ["ALBターゲット群", "HealthCheckProtocol / Port / Path", "HTTPまたはHTTPS／traffic-portまたはポート／URI", "例 HTTP・traffic-port・/readyz", "例ではフロント8080。実際の通信方式とリスナーを確認して置き換える。", "S07 S09"],
    ["ALBターゲット群", "TargetType", "今回のawsvpcではip", "ip", "ALBはlocalhostではなくタスクENIのIPとフロントのポートへ接続する。", "S12 S13"],
    ["ALBターゲット群", "deregistration_delay.timeout_seconds", "0～3600／既定300", "既存値維持", "停止時の処理中リクエストを排出する待ち。起動時猶予ではない。", "S10 S11"],
    ["ALBターゲット群", "slow_start.duration_seconds", "0（無効）または30～900／既定0", "まず0。負荷暖機が必要なら実測で60等", "healthy後の配信量を増やす機能。起動失敗を隠すものではない。", "S10 S11"],
    ["対象外の混同", "Docker --start-interval", "Docker Engineの別機能", "ECS healthCheckには設定しない", "ECS公開APIにstartIntervalフィールドはない。Dockerの既定値をFargateへそのまま当てはめない。", "S01 S29"],
    ["Fargate Linux", "機能を使えるplatform version", "コンテナhealthは1.1.0以上、依存・timeoutは1.3.0以上", "利用中のプラットフォームを確認", "これは機能の最低対応版。最新プラットフォーム番号の指定や更新の推奨ではない。", "S01 S04"],
], headers=["設定場所","正式名","許容範囲・既定","今回の具体値","意味・注意","根拠"], widths=[19,37,30,32,59,13])

section("04_時計と判定", "違う時計を一つにしない", "起動の時間軸、検査結果、ECSによる交換、ALBによる配信を分けて読むと、300秒に関する誤解を解消できます。", [
    ["コンテナの時計", "各startPeriodはそのコンテナの起動に対して働く。依存待ちでまだ開始されていないフロントの起動猶予を、タスク作成時刻から消費するとは扱わない。", "バックが100秒後に始まれば、バックの210秒はその起動から考える。フロントを並列で早く始めると、バック待ち時間を自分の猶予に含める。", "S01 S03"],
    ["ECSサービスの時計", "AWSの表現は『タスクが初めて起動した後』。Task.startedAtはタスクがRUNNINGになった時刻を表す。CreateService/RunTask呼出時刻とは区別する。", "図は最初のコンテナ開始を便宜上t0にする。t0＝ECS猶予開始と断定せず、試算では開始差を0に置く保守的比較とする。実測時はstartedAtとイベントを突き合わせる。", "S05 S15 S16"],
    ["ALBの時計", "ターゲット登録とリスナールール等の条件が整うとALBは定期検査する。ECS猶予300秒の満了を待って初めて検査する仕組みではない。", "起動中はALBがunhealthyでも、ECSが猶予により交換を控えることがある。300秒満了で失敗カウンターがリセットされるわけでもない。", "S05 S07"],
    ["依存先待ちの時計", "HEALTHY依存は依存先の正常化を待つための期限を別に持つ。API例ではAがBを待つときBにstartTimeoutを設定する。", "P1はADOTに120秒。P3/P4はADOTとバックに120秒。フロントだけに120秒を付ければバック待ちが延びる、と解釈しない。", "S04 S25"],
    ["早期成功の例", "startPeriod210、interval10、短時間で返る検査を仮定。10～70秒の失敗は数えず、80秒の成功でHEALTHY。90・100・110秒に連続失敗すれば、210秒前でもUNHEALTHYになり得る。", "10秒刻みは説明用。実ランタイムの実行位相や実行時間は変動する。一度200を返すreadinessは、本当に準備が整った時だけにする。", "S01 S29"],
    ["一度も成功しない例", "startPeriodを過ぎても自動的にHEALTHYにはならない。その後の連続失敗が閾値に達すればUNHEALTHYになる。", "210＋10×3＝240秒で必ず停止、と断定しない。検査実行時間・位相・ECS猶予・通知遅れ・交換処理が別にある。", "S01 S05"],
    ["4つのessential", "ヘルスチェックを定義したessentialコンテナのうち一つでもUNHEALTHYならタスクはUNHEALTHY。異常がなくUNKNOWNが残ればタスクもUNKNOWN。", "依存のないCW Agentも健康判定に参加する。全部trueにするとは、観測用コンテナにもタスク可用性を左右させること。", "S02"],
    ["健康と終了の違い", "プロセスが動いたまま検査だけ失敗する場合と、essentialプロセスが終了する場合は異なる。後者は原則タスク停止に結び付く。", "startPeriodやサービス猶予でクラッシュ・OOM・設定エラー・依存タイムアウトを保護できない。restartPolicyを有効化する場合は終了時の挙動を別途検証する。", "S04 S40"],
    ["配信と交換の違い", "ALBはALB自身のターゲット健康状態に基づいて配信する。ECSが全コンテナをHEALTHYと認識するまで必ず配信を止める、という連動ではない。", "アプリの受付制御をreadinessに実装する。ECSのminimumHealthyPercent集計では、必要なコンテナヘルスとALBヘルスの両方を待つ。", "S07 S14"],
    ["ALB fail-open", "利用可能なターゲットが全てunhealthyになるなどの条件では、ALBがunhealthyにもリクエストを送る場合がある。", "『unhealthyなら利用者は絶対に来ない』を前提にしない。旧正常タスクを残し、未準備時はアプリも503等で適切に応答する。", "S07 S10"],
])

def calculate(pattern, values=None):
    v = {key: value for key, _, value, *_ in INPUTS}
    if values:
        v.update(values)
    a_ready = sum(v[k] for k in ["a_process", "a_config", "a_receiver", "a_publish"])
    c_ready = sum(v[k] for k in ["c_process", "c_config", "c_visible"])
    aq = v["a_interval"] + v["a_timeout"]
    bq = pattern["b_i"] + pattern["b_t"]
    fq = v["f_interval"] + v["f_timeout"]
    cq = v["c_interval"] + v["c_timeout"]
    b_duration = v["b_max"] + (v["b_var"] if pattern["use_buffer"] else 0) + v["b_pre"] + v["b_post"]
    f_duration = v["f_max"] + (v["f_var"] if pattern["use_buffer"] else 0) + v["f_pre"] + v["f_post"]
    ah = a_ready + aq
    ch = c_ready + cq
    bs = 0 if pattern["mode"] == "parallel" else ah
    br = bs + b_duration
    bh = br + bq
    fs = bh if pattern["mode"] == "serial" else (ah if pattern["mode"] in ["start", "siblings"] else 0)
    fr = fs + f_duration
    endpoint = max(br, fr)
    fh = endpoint + fq
    task = max(ah, ch, bh, fh)
    alb_budget = v["alb_interval"] * v["alb_healthy"] + v["alb_timeout"]
    alb = endpoint + alb_budget
    service = max(task, alb) + v["registration"] + v["ecs_report"]
    spare = v["extra_failures"] * v["alb_interval"] + v["extra_control"] + v["observation"]
    required = max(0, service + spare - v["grace_origin"])
    dependency_ok = (pattern["mode"] == "parallel" or ah < v["a_start_timeout"]) and (pattern["mode"] != "serial" or b_duration + bq < v["b_start_timeout"])
    return dict(a_ready=a_ready,c_ready=c_ready,aq=aq,bq=bq,fq=fq,cq=cq,a_h=ah,c_h=ch,b_duration=b_duration,f_duration=f_duration,b_start=bs,b_ready=br,b_h=bh,f_start=fs,f_own=fr,endpoint=endpoint,f_h=fh,task=task,alb_budget=alb_budget,alb=alb,service=service,spare=spare,required=required,dependency_ok=dependency_ok,b_gate=b_duration+bq,f_local=fh-fs,grace_left=pattern["grace"]-required)

section("05_依存の設計", "dependsOnと120秒の関係", "『フロントからバックへの起動依存』と『フロントの正常判定でバックを参照すること』は、似て見えても別の仕組みです。", [
    ["P1の矢印", "ADOT ─HEALTHY→ バック。フロントは独立して起動し、正常判定だけでバックを確認する。CW Agentも独立して開始。", "矢印は『依存先→待つ側』。タスク定義のdependsOnは待つ側に書く。ADOT自身のstartTimeout=120はADOTを待つ側に適用される期限の設定。", "S03 S04"],
    ["P3の矢印", "ADOT ─HEALTHY→ バック ─HEALTHY→ フロント。CW Agentは別枝。", "ADOTの正常化待ちとバックの正常化待ちを別々に点検。各待ちが120秒以内でも、全体の所要時間は合計で120秒を超え得る。", "S03 S25"],
    ["160秒が問題になる理由", "ユーザーのバックの見積もり160秒に、ログ外の仮予算20秒と速い検査予算8秒を足すと188秒。バックのstartTimeout=120では68秒不足する。", "startPeriod=210自体は有効な設定でも、依存先待ちの上限を拡張しない。猶予600秒も同じ。", "S01 S04 計算"],
    ["80秒で成功する場合", "バックの実測最大80秒＋ログ外20秒＋検査8秒＝108秒。このモデルでは120秒まで12秒残る。", "『今まで成功した』と『160秒まで遅れても保護できる』を分ける。80秒という過去最大を超える起動を試験する。", "ユーザー 計算"],
    ["STARTという選択", "STARTは依存先のコンテナ開始を待つ。初期化やHTTP受付まで待つ条件ではない。P5ではフロントのアプリ側がバック未準備に耐える必要がある。", "単にHEALTHYをSTARTへ変えて、起動直後のバック呼出エラーを無視するのは不可。接続失敗を許容し、期限付きで再試行する設計が必要。", "S03 設計"],
    ["HEALTHYは起動時だけ", "起動後に依存先がUNHEALTHYになっても、dependsOnがもう一度フロントを待機状態に戻すわけではない。", "継続監視はコンテナヘルスとALBが担当。4つともessentialなので、異常や終了がタスク交換につながる。", "S02 S03"],
    ["正常化の意味", "ADOTのHEALTHYは設定した検査の成功に過ぎない。13133の200だけで、全トレースの外部配送成功まで証明することはできない。", "受信口、送信キュー、IAM、外向き通信、送信先エラー、アプリSDKの再試行を別に確認する。", "S18 S20 S22"],
    ["循環依存を避ける", "バックがフロントHEALTHYを待ち、フロントがバックHEALTHYを待つと、どちらも始められない。", "ADOTのhealthがバック起動を必須にするなど、検査内容に隠れた循環も作らない。", "設計"],
    ["停止順も変わる", "ECSの依存関係は停止時に逆になる。P3はフロント→バック→ADOTの順序制約を作る。P1はバック→ADOTだけで、フロントとの停止順は規定しない。", "フロントもトレースするならP6を検討。最後のトレース送信・flushとstopTimeout、ALBのdrainは別途実測する。", "S03 S04"],
    ["表記を取り違えない", "ECS JSONはdependsOn / containerName / condition。CloudFormationのコンテナ内はDependsOn / ContainerName / Condition。", "Terraformはcontainer_definitions=jsonencode(...)の中にdependsOnを書く。リソースのdepends_onはインフラ作成順であり、コンテナ起動順ではない。", "S26 S28"],
])

section("06_バッファ内訳", "P1：バッファを分解して秒数を出す", "160秒・140秒に含まれるユーザー予備を一度だけ加算します。それ以外の数値は、測定区間外を説明するための仮予算です。見積もりの倍数をさらに掛け直していません。", [
    ["B01", "バック：測定区間", "80（実測最大）＋80（変動予備）", 160, "ユーザーの2倍見積もりそのもの。", "ユーザー"],
    ["B02", "バック：測定区間外", "開始前10＋デプロイ後の安定受付10", 20, "仮定。entrypoint処理と実際のHTTP受付との差。イメージpull時間は含めない。", "仮定"],
    ["B03", "バック：自分の準備合計", "160＋20", 180, "バックコンテナ開始→API受付可能。ADOT待ちはバック開始前なのでここに足さない。", "計算"],
    ["B04", "バック：ECS検出予算", "interval10＋timeout5", 15, "短時間の正常応答を含めて置く設計予算。厳密な実時間上限ではない。", "S01 設計"],
    ["B05", "バック：最初のHEALTHYまで", "180＋15", 195, "バック自身の起動から195秒を見込む。", "計算"],
    ["B06", "バック：startPeriodの端数余裕", "210－195", 15, "設定210秒。起動前のADOT待ち38秒を再加算しない。", "提案"],
    ["F01", "フロント：測定区間", "70（実測最大）＋70（変動予備）", 140, "ユーザーの2倍見積もりそのもの。", "ユーザー"],
    ["F02", "フロント：測定区間外", "開始前10＋デプロイ後の自分の受付10", 20, "仮定。バック待ちは含めない。", "仮定"],
    ["F03", "フロント：自分の準備合計", "140＋20", 160, "フロントコンテナ開始→フロント自身の受付可能。", "計算"],
    ["A01", "ADOT：応答準備", "プロセス準備5＋設定10＋receiver10＋health公開5", 30, "全て未実測の仮予算。13133とOTLPの実測で差し替える。", "仮定"],
    ["A02", "ADOT：ECS検出予算", "interval5＋timeout3", 8, "初回正常化の検出予算。", "設計"],
    ["A03", "ADOT：HEALTHY・バック開始", "30＋8", 38, "P1ではt0から38秒でバックが始まるモデル。状態伝播の細部は実測対象。", "計算"],
    ["A04", "ADOT：startPeriodの端数余裕", "45－38", 7, "設定45秒。startTimeout120に対して82秒の余裕。", "提案"],
    ["F04", "バックAPIが使える時刻", "ADOT待ち38＋バック準備180", 218, "t0基準。フロントがバックのECS HEALTHYを待つわけではなく、APIの応答を直接見る。", "計算"],
    ["F05", "並列後に残るバック待ち", "MAX(0, 218－フロント自身160)", 58, "160秒と218秒を足さない。両者のうち遅い方まで58秒だけ追加で待つ。", "計算"],
    ["F06", "フロント複合ヘルスの検出", "MAX(160,218)＋interval10＋timeout5", 233, "フロントHEALTHYの計画時刻。ALBはこのECS判定時刻を待たず独自に検査する。", "計算"],
    ["F07", "フロント：startPeriodの端数余裕", "240－233", 7, "設定240秒。現在210秒では計画上の233秒まで23秒足りず、一部の失敗を数える可能性。", "提案"],
    ["C01", "CW：プロセス確認準備", "開始準備5＋設定処理10＋対象プロセス確認5", 20, "仮定。プロセスの存在を判定するだけで、CloudWatchへの配送を証明しない。", "仮定"],
    ["C02", "CW：HEALTHYと猶予余裕", "20＋interval10＋timeout5＝35、60－35＝25", 60, "startPeriod60秒。CWは並列なので全体へ35秒を足さずMAXに入れる。", "計算・提案"],
    ["G01", "ALB：回復検出予算", "interval10×正常2回＋応答予算5", 25, "unhealthyからの回復を保守的に採用。初回登録の1成功だけなら15秒予算となる。", "S08 設計"],
    ["G02", "ALB健康＋通常反映", "MAX(タスク正常233, API準備218＋ALB25)＋登録反映10＋ECS反映10", 263, "登録と反映は仮予算。実際には一部重なるため、ここでは重ならない側に見込む。", "計算・仮定"],
    ["G03", "追加予備① 一時検査失敗", "追加失敗3回×interval10", 30, "最大3周期分の追加遅れを設計上予約。AWSが失敗を3回だけに限定する意味ではない。", "方針"],
    ["G04", "追加予備② 制御面超過", "通常反映20秒を超える分として追加20", 20, "未実測の追加枠。起動80/70秒の変動予備とは異なる対象。", "方針"],
    ["G05", "追加予備③ 観測誤差", "ログ・状態採取の時間差に10", 10, "未実測。時刻計測の分解能が確定すれば縮小できる。", "方針"],
    ["G06", "ECS猶予：端数処理前", "263＋30＋20＋10－猶予開始差0", 323, "0は図t0と猶予開始を同一とする保守的な入力。実環境の開始差で再計算する。", "計算"],
    ["G07", "ECS猶予：端数余裕", "60秒単位の切上げ360－323", 37, "提案360秒。300秒との差は60秒だが、必要見積もり323秒との差は23秒。", "提案"],
    ["G08", "300秒の評価", "300－263＝37、300－323＝－23", -23, "通常モデルでは間に合う例。追加予備を全て要求すると23秒不足する。300秒で必ず失敗すると断定しない。", "計算"],
], headers=["ID","内訳","計算式","結果（秒）","根拠・解釈","区分"], widths=[9,31,53,14,64,17])

section("07_パターン比較", "7パターンの採否と具体値", "A=ADOT、C=CloudWatch Agent、B=バック、F=フロント。全パターンでessential=trueを維持。P4は制約を説明するための不採用例です。", [
    [p["id"],p["name"],f'A{p["a_sp"]} / C{p["c_sp"]} / B{p["b_sp"]} / F{p["f_sp"]}',p["grace"],f'B: {p["b_dep"]}\nF: {p["f_dep"]}',p["decision"]+"。"+p["note"],"設計 S03 S04"] for p in PATTERNS
], headers=["ID","方式","startPeriod（秒）","ECS猶予（秒）","dependsOn","採用条件と注意","根拠"], widths=[8,30,32,16,34,65,17])

setting_rows=[]
for p in PATTERNS:
    for key,label,sp,interval,timeout,dep,start_timeout in [
        ("adot","ADOT",p["a_sp"],5,3,"なし","設定不要" if p["mode"]=="parallel" else "120"),
        ("cwagent","CW Agent",p["c_sp"],10,5,"なし","設定不要"),
        ("backend","バック",p["b_sp"],p["b_i"],p["b_t"],p["b_dep"],"120" if p["mode"]=="serial" else "設定不要"),
        ("frontend","フロント",p["f_sp"],10,5,p["f_dep"],"設定不要")]:
        setting_rows.append([p["id"],label,sp,interval,timeout,3,"true",dep,start_timeout])
section("08_全コンテナ値", "各パターン・各コンテナの全設定", "全て秒単位（retriesは回数）。startTimeoutはHEALTHY等を待たれる依存先に設定します。P4は値域上有効でも依存時間の設計が成立しません。", setting_rows,
        headers=["方式","コンテナ","startPeriod","interval","timeout","retries","essential","dependsOn","startTimeout"],widths=[8,17,15,12,12,11,13,35,28])

time_rows=[]
for p in PATTERNS:
    m=calculate(p)
    time_rows.append([p["id"],m["b_start"],m["b_ready"],m["b_h"],m["f_start"],m["endpoint"],m["f_h"],m["service"],m["required"],"成立条件あり" if m["dependency_ok"] else "不成立（後半は仮想）"])
section("09_時間軸の読み方", "時間軸を秒で比較する", "t0=最初のコンテナ開始の説明用基準。各数値は実測予測ではなく、内訳を積み上げた計画値です。図の時計とECS猶予の開始は同一と断定しません。", time_rows,
        headers=["方式","B開始","B API準備","B HEALTHY","F開始","複合API準備","F HEALTHY","通常完了予算","追加予備込み","依存制約"], widths=[8,12,14,14,12,16,16,18,18,27])

section("10_計算の解説", "計算式・二重計上・300秒の読み替え", "Excelの『21_秒数試算』は白い太枠の入力を変更するとP1の数値を再計算します。固定の比較表は初期条件のスナップショットです。", [
    ["記号", "A＝ADOTのHEALTHYまで38。B＝バック自身の準備180。F＝フロント自身の準備160。qB=qF=15。C＝CW HEALTHYまで35。", "全て起動区間をそろえて扱う。JBossログの区間160/140と、コンテナの区間180/160は同じではない。", "計算"],
    ["並列と直列", "P1の複合API準備＝MAX(F, A+B)＝MAX(160,38+180)＝218。仮に直列ならF開始＝A+B+qBとなり、その後Fを足す。", "同時に走る仕事はMAX（遅い方）。待ってから始める仕事は足し算。この違いだけで待ち時間が変わる。", "計算"],
    ["ECSとALBの検出", "P1のF HEALTHY＝218+15=233。ALB healthyの予算＝218+25=243。両方がそろう側を選び、登録・状態反映20秒を足して263。", "ALBがF HEALTHY233を受け取ってからさらに25秒待つ、とは計算しない。ALBは独立して検査するため。", "S07 S14 計算"],
    ["猶予の余裕", "P1の追加予備＝一時失敗30＋制御面超過20＋観測10＝60。263+60=323。60秒刻みに切り上げ360。", "360はAWS推奨の固定値ではなく、この資料の仮予算から選んだ初期値。未実測入力が増えれば再計算する。", "設計"],
    ["現状300を維持できる例", "P0は計画225＋予備60=285で300内。P2は183＋60=243で300内。P1は通常263だが予備込み323。", "P0はADOTへの早期送信リスク、P2は2倍変動予備を外す条件がある。数字だけで一律に方式を入れ替えない。", "計算"],
    ["現在Fの210秒", "P1のF初回正常検出予算233秒と比べると23秒短い。ただし、210秒後に即UNHEALTHYや即停止になるわけではない。", "retriesとサービス猶予で間に合う場合はある。起動設計を偶然のチェック位相へ依存させず、FのstartPeriod240を初期案とする。", "S01 S05 計算"],
    ["元の300秒の想定", "『バックのstartPeriodが満了→フロント開始→300秒でALB初回検査』という連鎖は起きるとは限らず、設定の意味とも異なる。", "バックが実際に早く200を返せば早くHEALTHY。ALBは登録後から検査する。バックが非常に遅いなら先に依存startTimeoutが問題になる。", "S01 S04 S07"],
    ["JBoss/EAP時間の区別", "イメージpullやタスク準備は、アプリログより前にある。コンテナ開始後の設定展開はpreに、デプロイ後からAPI安定までをpostに入れる。", "配備操作→サービス安定の総時間を出すときは、pull・ENI準備・依存・旧タスクdrainも別に集計する。全てをサービス猶予に無条件で足さない。", "S15 S16"],
    ["上限でないこと", "interval+timeoutはこの資料の検出予算。実行位相・CPU遅延・再試行・伝播遅延により延び得る。ALBのI×Hも簡略化した予算。", "秒数計算は予算の見える化。実環境で最大時間や確率を保証する統計モデルではない。合否は実測と異常注入で判断する。", "設計"],
    ["倍の余裕の重複防止", "バックの160にさらに『起動変動80』を足すと、同じ余裕を二度入れて240にしてしまう。本資料は80+80で一回のみ。", "FにB180とF160の両方を足すのもP1では誤り。ADOT38はB自身のstartPeriodには不要だが、先に始まるFの複合healthには影響する。", "計算"],
])

section("11_ヘルス経路", "フロントのチェックを正しくする", "『どのコンテナでコマンドを動かすか』と『どのアプリを検査しているか』は違います。同一タスクのlocalhostにはバックのポートもあります。", [
    ["現行の検査", "フロント内の検査コマンド → https://localhost:18080/iwinmichl/healthcheck → バックのSpringコントローラ → 200を確認。", "分かることはバックの指定経路が応答すること。フロント自身の受付、JBossのデプロイ、外部からの接続までは分からない。", "ユーザー S12"],
    ["反例", "バックだけ正常で、フロントのJBossが起動途中／ポート未listen／要求処理が停止している状態でも、検査コマンドがバックを呼べれば成功し得る。", "essential=trueだけではこの誤判定を防げない。アプリプロセスが生きているがHTTPだけ壊れる例を試験する。", "設計"],
    ["推奨の入口", "例としてフロントの8080に/readyzを設ける。フロントの通常のHTTP処理経路で受付でき、必要な初期化が完了し、バックAPIも短い期限で200なら200。", "8080と/readyzは新設する場合の例。フロントもHTTPSならその方式に変更する。ALBとコンテナの両方がこの経路を見る。", "設計"],
    ["バックの入口", "既存の/iwinmichl/healthcheckを利用できるが、単に固定200を返すだけか、業務受付に必要な準備が終わっているかを確認する。", "Springコントローラがロード済みでも、別スレッドの初期化・キャッシュ・設定読込が残るなら、その準備フラグも含める。", "設計 S31 S32"],
    ["成功・未準備", "準備完了だけ200。未準備や必須の同一タスク内バックが使えない場合は503。例外やタイムアウトを200へ変換しない。", "302ログイン画面、404、401、403を健康と認めない。HTTPボディに内部情報や秘密を載せる必要はない。", "設計 S07"],
    ["チェック自体を軽くする", "DBの大きな検索、外部APIの長い呼出、書込や副作用を伴う処理をhealthcheckに入れない。バックへの確認は短い期限で打ち切る。", "10秒おきに複数経路から呼ばれても負荷にならないものにする。ALBは複数ノードから検査するため、厳密に毎10秒1回とは限らない。", "S07 設計"],
    ["二段チェック案", "フロントの/readyz実装がまだない場合、検査スクリプトで①フロント自身の小さい応答、②バックの200を順に確認する。両方成功した時だけ終了コード0。", "各curlの全体上限2秒なら2回で最大約4秒。ECS timeout5秒に実行余白を残す。重い初期化を検査コマンドに書かない。", "S01 S30 設計"],
    ["ALBも同じ品質で検査", "ALBの送信先はタスクENI:フロントport。フロントが自分とバックの利用可否を評価する経路にする。", "ALBをバック18080へ直接向けると、フロントが壊れていてもターゲット正常になる。/readyzの実装とリバースプロキシ設定を整合させる。", "S07 S13 設計"],
    ["localhostとTLS", "同じタスクならlocalhost通信は可能。ただしhttps://localhostの証明書にlocalhostのSANがなければ名前検証で失敗する。IPv6の::1とIPv4のみlistenの差にも注意。", "信頼するCAを入れ、証明書名に合うURLと--resolve等を使う。-k/--insecureを恒久対応にしない。ALB経由のTLSとは別の確認。", "S12 S30"],
    ["タイムアウトの階層", "例：バックへのhealth呼出は2秒以内、フロント/readyzも4秒以内、コンテナ検査timeout5秒、ALB timeout5秒。", "内側の呼出が外側の期限より長いと、検査元が先に諦める。実際のreadinessの応答分布に合わせて調整する。", "設計"],
    ["readinessとliveness", "『利用者を受けてよいか』と『再起動で直るほど自分が壊れたか』は目的が違う。ECSのコンテナhealthは異常時のタスク交換にも使われる。", "共有DB障害を全コンテナの致命的異常にすると一斉交換になり得る。今回の必須・同一タスクのバックと、共有外部依存を区別する。", "S02 S41 設計"],
    ["EAPとSpringの差", "EAPのバージョンやXP導入で管理healthの機能は異なる。Springコントローラがあることだけから、Spring Boot Actuatorが使えると決めない。", "/actuator/health/readinessや管理ポート9990を無条件に採用せず、実際のアプリ版・依存・公開範囲を調べる。", "S31 S32 S41"],
])

section("12_サイドカー", "ADOTとCloudWatch Agentの注意点", "ヘルスチェックは『その検査で確かめたこと』しか保証しません。プロセス確認とメトリクス・トレースの最終到達を区別します。", [
    ["ADOT 13133", "例：health_check extensionを127.0.0.1:13133、path /で定義し、service.extensionsにも登録する。ポート番号を宣言するだけではサーバーは動かない。", "HTTPの200を確認。HTTPSとしてアクセスする設定ではない。OTLP 4317/4318等の受信ポートとは役割が異なる。", "S18 S20 S21"],
    ["ADOTの検査実行", "公式ソースのイメージには/healthcheckが同梱され、その実装は127.0.0.1:13133の/をHTTPで確認する。", "例は[CMD, /healthcheck]。採用するタグ・digestにもその実体があることを確認する。scratchなのでcurlや/bin/shを当然に使わない。", "S18 S19"],
    ["HEALTHY待ちの効果", "バックをADOTの初回正常化後に起動することで、受信プロセスが全く起動していない時間帯の送信を減らせる。", "13133での正常と、利用するreceiverの受付・認証・外部exportの成功は別に検証。『確実にロスゼロ』という表現は避ける。", "S18 S20 S22"],
    ["トレースロスの残り方", "SDKのキュー溢れ、未送信のまま終了、Collector送信キュー溢れ、権限不備、NAT/VPC endpoint、exporterエラー、送信先停止でもロスは起き得る。", "SDK/Collectorの期限付き再試行・キュー容量・flushを確認。永続キューもタスク破棄時の保存先を考慮しないと恒久保全にはならない。", "S22 設計"],
    ["古いpipeline検査", "参照した上流health_checkのREADMEは、check_collector_pipelineが期待どおり動かない旨を記載している。上流に新方式があってもADOTの採用版にあるとは限らない。", "その設定を有効化したからend-to-endの送信が証明できる、としない。実際のCollectorのコンポーネントとバージョンを固定して試験する。", "S20"],
    ["ADOTが120秒以上", "依存先ADOTがHEALTHYになるのに120秒以上必要なら、P1でもHEALTHY依存が成立しない。startPeriod300にしても救済しない。", "ADOTの初期化を短縮するか、アプリを起動させた上で有限待機・再試行・保持を実装する別設計が必要。未準備中のトレースを単に捨てない。", "S04 S22 設計"],
    ["CWのプロセス検査", "対象はCloudWatch Agent本体のプロセス。コマンドラインの部分一致だけで自分のpgrep/grepを拾わないようにする。", "静的な専用プローブ等で/procの実行ファイルを厳密に確認し、ゾンビ状態を成功にしない。PID名前空間を共有している場合も対象を限定する。", "S25 設計"],
    ["CWイメージの罠", "参照した公式Dockerfileの最終段はscratchで、amazon-cloudwatch-agent-ctlも除去されている。shell、pgrep、curlを使える前提にできない。", "現行のプロセス確認が動くカスタムイメージなら維持する。例の専用チェックは事前に自作・同梱する。存在しないコマンドを設定しない。", "S23"],
    ["プロセス確認の限界", "Agent本体が存在しても、設定不正後の処理停滞・権限不足・CloudWatch配送失敗は見落とすことがある。", "healthはプロセス確認、監視はAgentログ・配送エラー・メトリクス欠落を別に観測する。依存なしは同時開始を意味し、先に準備完了する保証ではない。", "設計"],
    ["procstatと混同しない", "CloudWatchのprocstatプラグインはECS Fargateでは非対応とされる。今回の『自コンテナのAgentプロセスを調べるhealthコマンド』とは別の話。", "Fargateでprocstatを有効化すればこのhealthcheckが実現する、とは説明しない。", "S24"],
    ["4つともessentialの判断", "この資料では要求どおり4つともtrue。観測用Agentの異常にもタスクの健康や停止が影響される。", "将来falseを検討する場合は、観測欠落時もアプリを続ける運用方針が必要。今回勝手にfalseへ変更する提案にはしない。", "S02 S04"],
    ["ポート重複", "awsvpcの同一タスクはネットワーク空間を共有する。ADOTとCW Agentの両方で同じ4317/4318/13133等をlistenさせると競合し得る。", "CWがOTLP受信も担当する設定なら、今回のADOTとの役割・bindアドレス・ポートを明示的に分ける。", "S12 設計"],
])

section("13_ALBとサービス", "ALB側とECSサービス側の具体的設定", "ALBの検査設定とECSサービスの猶予は別の設定画面・APIにあります。300秒という同じ数字でも用途が違います。", [
    ["P1 ECSサービス", "healthCheckGracePeriodSeconds=360。起動失敗の無視対象はELBだけでなくコンテナ等の異常healthも含む。", "即時終了、依存タイムアウト、配置失敗を無視する機能ではない。余分な実行タスクを減らす時に猶予中の異常タスクが止まる例外もある。", "S05 S06"],
    ["P1 ALBターゲット群", "HealthCheckIntervalSeconds=10、HealthCheckTimeoutSeconds=5、HealthyThresholdCount=2、UnhealthyThresholdCount=3、Matcher.HttpCode=200。", "HealthCheckPath=/readyz、HealthCheckPort=traffic-port。例のフロントがHTTP8080ならProtocol/HealthCheckProtocol=HTTP、TargetType=ip。", "S07 S09 S13"],
    ["新規登録の最初", "ECSの最適化資料では、新規登録のターゲットの初回正常化には正常閾値にかかわらず1回の成功を用いる。", "本資料の猶予試算は起動中に一度unhealthyになってから回復するケースを取り、2回成功の25秒予算で評価する。", "S08"],
    ["初期値のままなら", "間隔30・正常閾値5でunhealthyから回復する場合、成功回数の待ちだけでも約150秒の枠になる。提案例10×2では約20秒。", "1回の応答時間、登録反映、チェック位相は別。『初期化が終わっているのに配備が長い』原因になり得る。", "S08"],
    ["intervalを300にしない理由", "間隔を延ばすと起動後の本当の故障の発見や復帰も遅れる。検査開始まで300秒待機という指定ではない。", "起動失敗への配慮はstartPeriodとservice graceで表し、定常時の検出感度はintervalとthresholdで決める。", "設計 S01 S07"],
    ["graceを長くする代償", "異常healthを理由に交換すべき新タスクが、猶予中は残りやすくなる。失敗したデプロイの見極めも遅れることがある。", "P1の360は根拠つきの初期案。多数回の測定後に300へ戻せるかを評価する。無制限に長くしない。", "S05 設計"],
    ["既存タスクを残す", "ECSローリング更新ならminimumHealthyPercent=100、maximumPercent=200を候補とし、新タスクの正常化まで旧タスクを維持できる容量を確保する。", "desiredCount、空きIP、CPU/メモリ枠等により実行可能性は変わる。CodeDeploy等の別方式に同じ説明をそのまま適用しない。", "S14"],
    ["登録解除待ち300", "deregistration_delay.timeout_seconds=300は停止するターゲットの処理中接続のための待ち。起動時のサービス猶予に加算されるものではない。", "長いリクエストやWebSocketの運用に関わるため、起動を速くしたい理由だけで短縮しない。", "S10 S11"],
    ["slow start", "healthyになったターゲットへ、徐々に配信量を増やす。JVMの暖機やキャッシュが問題なら追加検討できる。", "初期化前の健康判定を代替しない。今回の基本案は0。利用する場合はルーティング方式等の対応条件も確認する。", "S10"],
    ["更新方法の違い", "サービス猶予の更新自体は新しいデプロイを起こさない。コンテナhealthやdependsOn変更は新タスク定義リビジョンを作り、それを使うタスクへ切り替える。", "現在の起動済みコンテナのstartPeriodをその場で変更したつもりにならない。承認済みの配備手順で段階的に変更する。", "S05 S25"],
])

section("14_異常時の動き", "何が壊れるとどうなるか", "ヘルスチェックの失敗と、コンテナの終了、依存タイムアウトを別々に試験します。時刻はAPIの瞬時反映を保証するものではありません。", [
    ["起動中、まだ200なし", "startPeriod内の失敗は初期連続失敗数に含めない。ALBは独立に異常を観測し得る。", "ECSの猶予内で起動を続けられるかを観測。依存待ちの上限とプロセス終了は別に監視する。", "S01 S05"],
    ["一度200の後に失敗", "startPeriod中でも失敗カウントが始まる。3回連続失敗ならコンテナUNHEALTHYになり得る。", "『最初の200が早すぎた』readiness実装を疑う。実起動時の短い成功を合格にしないことが大事。", "S01"],
    ["バックが150秒超", "P1はバック210秒の猶予内で扱える可能性。P3は依存先startTimeout120を超える可能性。", "実測の80秒だけで成功確認せず、160秒の見積もりを使うならその遅延を非本番で試験する。", "S04 設計"],
    ["フロントが未準備", "バックだけへの検査は誤って成功し得る。フロントを通る/readyzなら未listen、503、タイムアウト等を観測する。", "ALBがバック直接を検査していないことも確認する。", "設計"],
    ["ADOTが健康にならない", "P1/P3/P5/P6はADOT依存が解けずバックが開始できない。startTimeout120で断念する方向になる。", "タスク停止理由とADOTログを読む。サービスgrace延長で対処しない。", "S04"],
    ["ADOTは200、送信先障害", "13133が200でもトレースの最終到達は失敗し得る。", "healthだけでなくexport失敗やキュー使用量、テストトレースの到達を確認。", "S18 S20 S22"],
    ["CWプロセスがない", "プロセス検査失敗が続けば、essentialのコンテナ異常がタスク健康へ反映される。", "プローブがそもそも存在しない／実行できないケースを先に排除する。", "S02 S23"],
    ["essentialが終了", "restartPolicyを使わない本資料ではタスク全体の停止につながる。", "猶予を延ばす前にOOM・不正設定・終了コード・entrypoint失敗を調べる。", "S04 S40"],
    ["猶予が満了", "その時点で続いている異常がサービスの交換判断に使われる。300秒時点でALBの初回検査を開始するわけではない。", "満了前からALBがunhealthyなら、その履歴を含めて観察。交換の正確な秒数を固定計算しない。", "S05 S07"],
    ["全部のターゲットが異常", "ALBがfail-openして異常ターゲットへ送る場合がある。", "アプリも未準備を503等で表し、正常な旧タスクを残す。起動中の実トラフィックの扱いを確認する。", "S07 S10"],
    ["依存先が運用中に異常", "dependsOnは再評価による起動待機を行わない。通常のhealthとECSサービスによる交換が働く。", "依存があるから継続的な障害連動が保証される、と思わない。", "S03"],
    ["共有DB・外部サービス障害", "すべてのタスクが同じ外部依存で異常になり、交換が繰り返される危険がある。", "その依存の失敗をreadiness・liveness・別アラームのどれに表すべきかを検討。今回の同一タスク内バックの必須性とは分ける。", "S41 設計"],
])

section("15_計測と検証手順", "実環境で確定するための手順", "この資料作成時にはAWS・JBossへの接続や配備を行っていません。以下は非本番で実施して設定を確定するための手順です。", [
    ["1 現物の設定を採取", "ECSサービスのhealthCheckGracePeriodSeconds、タスク定義のhealthCheck/dependsOn/startTimeout/essential、ALBのhealthと属性を採取。", "300秒がECS猶予か登録解除待ちかを確定。イメージはタグだけでなくdigest、EAP・Collector版も記録。秘密情報を資料に転記しない。", "S05 S10 S25"],
    ["2 時刻の基準を合わせる", "task createdAt / pullStartedAt / pullStoppedAt / startedAtと、コンテナごとのStartedAt、JBoss開始・完了ログを採取。", "UTCの時刻にそろえ、ログに時刻があるか、採取側時刻かを区別。同一task ARNで関連付ける。", "S15 S17"],
    ["3 必要な到達点を採取", "ADOT receiver listen、13133の最初の200、バックAPIの最初の安定200、フロント自身の200、複合200、ALB healthy、ECS task healthy。", "JBossデプロイ完了だけで終了しない。Container health状態の観測間隔も記録する。", "設計"],
    ["4 バッファを置換", "この資料のpre/post各10秒、ADOT30秒、CW20秒、制御面通常20秒、追加予備60秒を測定値と設計方針で更新。", "測定の二重計上がないか確認。計測数・CPU/メモリ・同時配備数・イメージサイズ・時間帯を記録する。", "設計"],
    ["5 並列の起動試験", "フロントが先、バックが先、ADOTが遅い、CPUが競合する組合せでP1を試験。", "フロントの初期化がバックへの1回の接続失敗で終了しないこと、未準備時に健康を返さないことを確認。", "設計"],
    ["6 境界試験", "バックの応答を120秒前後、見積もり160秒相当まで遅らせる。ADOTの初回healthを120秒近くまで遅らせる。", "P1とP3で異なる結果になる点を確かめる。長いsleepを本番に恒久導入せず、非本番の制御可能な方法を使う。", "S04 設計"],
    ["7 偽陽性試験", "バックだけ200、フロント自体は利用不能という状態を作り、フロントhealthとALBが成功しないことを確認。", "302/404/401、TLS名不一致、バック接続タイムアウト、frontendport間違いもチェック。", "設計"],
    ["8 早期成功後の異常", "startPeriod内に1回200を返し、その後連続失敗するケースを観測。", "startPeriod満了まで全失敗が無視されるという誤解が残らないよう、コンテナ状態とサービス判断を別々に記録。", "S01 S05"],
    ["9 サイドカー試験", "ADOTの外部送信だけ失敗させる、CWのプロセスを停止する、プローブの実行権限を確認する。", "13133の200とトレース到達が別であること、essentialにより起きる交換が運用方針どおりであることを確認。", "S02 S22"],
    ["10 配備完了と利用者", "旧タスクを残したローリング更新で、起動中に実トラフィックのエラーが増えないかを見る。", "検査成功だけで合格にせず、利用者向け5xx、応答時間、トレース到達、不要交換回数も評価する。", "S14 設計"],
    ["11 判断の基準", "P1ではADOTの初回正常化が120秒未満、B自身の初回健康が210秒以内、F自身の起動から複合健康が240秒以内を目標とする。", "サービスの必要時間がgrace内に収まり、追加予備の方針を満たすこと。チェック位相に依存してかろうじて通る結果を根拠にしない。", "設計"],
    ["12 失敗理由の切分け", "ECS停止理由、個別container reason/exitCode、ALB reason、アプリログを同じ時間帯で照合する。", "Target.Timeout＝時間不足とは限らない。listen、SG、TLS、パス、CPU停止等の可能性を比較する。", "S07 S15"],
])

section("16_歴史と背景", "なぜこれらの機能が別々に登場したか", "以下は公式発表で確認できる主な節目。サービスの登場順を知ると、ひとつのタイマーで全てを解決しようとしない理由が分かります。", [
    ["2016-08-11", "Application Load Balancerが登場", "アプリの入り口からHTTP等を調べ、利用可能な宛先へ分配する役割が重要になった。", "外からの経路を調べるALB healthと、内部の各コンテナの検査は別の役割。", "S36"],
    ["2017-11-29", "Fargateが登場", "コンテナを動かす基盤サーバーの準備や管理を利用者から切り離した。", "アプリやサイドカーの準備時間・依存関係は、引き続きタスク設計で考える必要がある。", "S37"],
    ["2017-12-14", "統合CloudWatch Agentが登場", "メトリクスとログを一つのAgentで集める仕組みが整備された。", "観測担当をアプリの隣へ置く構成につながる。現在のFargateサイドカーの対応範囲とは分けて読む。", "S38"],
    ["2017-12-27", "ECSのELB健康チェック猶予", "起動が遅いタスクをELBが異常と判断し、ECSが完成前に停止する問題を避けるために導入された。", "生まれたのはECS店長の猶予。ALB案内係の検査開始を遅らせるタイマーではない。", "S33"],
    ["2018-03-08", "ECSのコンテナhealthとタスクhealth", "ELBから見えるHTTP/TCPだけでなく、個々のコンテナ内部を明示的な検査で評価できるようになった。", "バック、ADOT、CWをそれぞれ調べ、essentialの結果をタスク健康へ反映する考え方。", "S34"],
    ["2018-03-24", "ALB slow start", "健康になったばかりのアプリへ負荷を少しずつ増やすための機能。", "準備時間の失敗を許す猶予と、準備後に負荷を暖機する機能が別であることが分かる。", "S36"],
    ["2019-03-07", "ECSの依存関係・個別timeout強化", "観測用コンテナを先に起動し後で停止する、初期化コンテナの完了を待つ等の順序を定義しやすくなった。", "今回のADOT→バックは、この発表が挙げる観測サイドカーの使い方に近い。依存の付け過ぎは直列化を招く。", "S35"],
    ["2020-10 / 2021-09-29", "ADOT preview / tracing GA", "OpenTelemetryによる計測・収集・配送をAWSで利用する選択肢が整備された。", "アプリ開始直後のトレースを受ける準備と、その後の配送の信頼性を別に設計する必要がある。", "S39"],
    [CHECKED, "今回の確認時点", "AWS公開API・開発者ガイドと公式ソースを確認。上流mainは将来変わるため、ADOT/CWの実装参照は確認したコミットへ固定した。", "ユーザーのイメージが同じ実装とは限らない。EAP等の最新版へ更新する提案や、最新イメージを本番へ無検証導入する提案ではない。", "調査"],
],headers=["時期","出来事","背景・解決したかった問題","今回へのつながり","根拠"],widths=[23,36,62,62,13])

section("17_FAQ", "今回の疑問への具体的な回答", "結論だけでなく、成立条件と例外も合わせて読むための早見表です。", [
    ["210秒を短くすれば速い？", "原則、成功を待つ速度は変わらない。210秒の間も検査し、成功すればHEALTHYになる。", "interval・実際の初期化・誤った依存関係の方が速度に直接影響する。猶予短縮は失敗への厳しさを変える。", "S01"],
    ["210＋210を足す？", "startPeriodの設定値は起動の固定待ちではないため、その合計420秒を実際の起動時間としない。", "直列の場合は実際の準備と正常検出を足す。並列はMAXで計算する。", "S01 計算"],
    ["300秒後にALB初回検査？", "ECS猶予なら違う。ALBは登録等の条件成立後から独立して検査する。", "300秒はECSによる異常healthを理由とする交換判断の猶予。", "S05 S07"],
    ["300秒は短過ぎる？", "条件次第。P0とP2の例は必要予算285秒と243秒。P1は通常263秒、追加予備を含め323秒。", "P1は360秒を初期提案。計測によって追加予備が少なくてよいなら300秒を再評価できる。", "計算"],
    ["バックstartPeriod160でよい？", "160秒がJBoss区間だけの予算なら、コンテナ開始からの時間と検出時間が含まれない可能性がある。", "本資料ではログ外20＋検出15を加え195、端数余裕15で210。実測でログ外がほぼ0なら小さくできる。", "計算"],
    ["フロントstartPeriod140でよい？", "P1では自分の140秒だけでなく、ADOT待ちを含んだバックの準備を確認する時間も必要。", "自分160とバック218の遅い方＋検出15で233。端数余裕7を付け240。", "計算"],
    ["ADOTは210秒に統一？", "統一する根拠はない。ここではADOTの仮準備30＋検出8から45を提案。", "ADOTをHEALTHY依存先にする以上、初回正常化がstartTimeout120以内である必要がある。", "S04 計算"],
    ["バックを160秒待ちたい", "FargateのHEALTHY依存のstartTimeoutに160は指定できない。", "P1/P6のように起動依存を外す、初期化を短縮する、P5でアプリ側の有限待機を実装する等を選ぶ。", "S04"],
    ["フロントからバックを見るだけで依存不要？", "起動を並列化することは可能。ただしフロントがバック未準備でも起動を継続でき、フロント自身も検査することが条件。", "healthcheckは起動処理を待機・再試行させる仕組みではない。フロント起動時の依存呼出が致命的ならアプリ側対応が必要。", "設計"],
    ["ADOT HEALTHYならトレースはロスなし？", "初期の受信準備前送信の危険は減らせるが、配送までの完全保証ではない。", "SDKの保持・再試行、Collectorのキュー、外部export、停止時flushを別に検証する。", "S20 S22"],
    ["CWは依存なしでよい？", "アプリがCWの即時受付を必須としていなければ、別枝として並列にできる。", "直接CWへ起動直後のデータを送る設計なら、欠落対策は別途必要。依存なしでもessential healthはタスクに影響する。", "S02 設計"],
    ["全部essential=trueでよい？", "観測系が動かなければタスクを交換する方針なら整合する。本資料では指定どおり維持。", "アプリ可用性を優先して観測欠落を許す方針へ変更する場合だけ、別途falseの影響を検討する。", "S04 設計"],
    ["HTTP200でなく302もよい？", "準備できた証拠にならないリダイレクトを合格にしない。", "ALB matcherは200。curlでも厳密に200を確認。-fだけでは3xxを排除できないため追加確認する。", "S07 S30"],
    ["バッファの2倍は統計的に正しい？", "少数の実測最大の2倍は保守的な設計方針であり、確率分布から求めた保証値ではない。", "件数・環境条件・同時配備・リソース負荷を増やして分布を測り、必要な余裕を決める。", "設計"],
    ["停止までの秒数も足せる？", "停止猶予、ALB drain、状態通知、交換処理は別の段階であり、必ず直列とは限らない。", "startPeriod＋retries×interval＋graceのような総和で、実停止時刻を断定しない。", "S01 S04 S05 S10"],
])

section("18_用語集", "用語と正式な設定名", "似た言葉を区別するための辞書です。", [
    ["ECS / Fargate", "ECSはタスクやサービスを管理する仕組み。Fargateはそのコンテナの実行基盤。", "この資料はECS上のFargateを対象とする。", "S37"],
    ["ELB / ALB", "ELBは負荷分散サービス群の総称、ALBはその一種類。", "今回の具体的なHTTP検査はALBターゲットグループに設定。", "S07"],
    ["タスク / サービス", "タスクは一緒に動かすコンテナのまとまり。サービスは必要数のタスクを維持する管理単位。", "単発RunTaskはサービスによる自動交換と同じではない。", "S01 S05"],
    ["healthCheck / healthStatus", "前者は検査の定義。後者はその結果のHEALTHY / UNHEALTHY / UNKNOWN等。", "アプリのHTTPコードとECSの状態名を混同しない。", "S01 S02"],
    ["startPeriod / startTimeout", "前者は自分の起動時検査失敗の猶予。後者は依存先の条件成立を待つ期限。", "許容上限は前者300秒、Fargateの後者120秒。", "S01 S04"],
    ["grace / drain", "graceは起動したタスクへの異常health判断の猶予。drainは停止する宛先の既存処理の排出。", "どちらも300秒を見かけるが設定場所も目的も違う。", "S05 S10"],
    ["essential", "そのコンテナをタスクの必須要素として扱う指定。", "今回の四つは全てtrue。綴りは単数形。", "S04"],
    ["readiness / liveness", "受付できるか／自分が動作可能か、という目的の違い。", "ECSではKubernetesの複数probeと同じ仕組みがそのまま存在するわけではない。", "S01 S41"],
    ["OTLP / receiver / exporter", "テレメトリの送受信方式／受信担当／外部送信担当。", "13133のhealthは4317/4318等のOTLP本体とは別の入口。", "S18 S21"],
    ["ENI / localhost", "タスクのネットワーク口／同一タスク内のローカル通信先。", "ALBはENIへ接続。フロント内のlocalhost:18080はバックを指し得る。", "S12"],
    ["実測 / 仮定 / 提案", "実測はユーザーが測った事実。仮定は未実測の試算入力。提案はその入力から選ぶ設定。", "Excelでは区分を表示。仮定の30秒や10秒をAWSの保証値として転記しない。", "本資料"],
])

BACKEND_SCRIPT = r'''#!/bin/sh
# Linuxアプリイメージに事前に配置し実行権限を付ける例。
# localhostが証明書SANに含まれ、CAを正しく配置した場合。
code=$(curl --silent --show-error --noproxy '*' \
  --connect-timeout 1 --max-time 2 \
  --cacert /etc/pki/health/ca.pem \
  --output /dev/null --write-out '%{http_code}' \
  'https://localhost:18080/iwinmichl/healthcheck') || exit 1
[ "$code" = '200' ] || exit 1
exit 0'''

FRONTEND_SCRIPT = r'''#!/bin/sh
# 8080と/readyzは例。フロント自身がバックの状態も評価する実装が前提。
code=$(curl --silent --show-error --noproxy '*' \
  --connect-timeout 1 --max-time 4 \
  --output /dev/null --write-out '%{http_code}' \
  'http://127.0.0.1:8080/readyz') || exit 1
[ "$code" = '200' ] || exit 1
exit 0'''

ADOT_CONFIG = '''# 既存Collector設定へ併合する断片。既存pipelineを消さない。
extensions:
  health_check:
    endpoint: "127.0.0.1:13133"
    path: "/"
service:
  extensions: [health_check]
# 既存のextensions一覧があれば、その一覧にhealth_checkを追加する。
# receivers/processors/exporters/pipelinesは既存の必要な設定を維持。
# 13133はHTTP health用。OTLP receiverは別途定義・有効化する。'''

READ_ONLY_POWERSHELL = r'''# 読み取りだけの例。識別子は自分の環境で設定する。
# 応答の環境変数・秘密情報をそのまま外部共有しない。
$ecsCluster = '<cluster-name>'
$ecsService = '<service-name>'
$ecsTaskDefinition = '<family:revision>'
$ecsTaskArn = '<task-arn>'
$targetGroupArn = '<target-group-arn>'
aws ecs describe-services --cluster $ecsCluster --services $ecsService --query 'services[].{grace:healthCheckGracePeriodSeconds,deployment:deploymentConfiguration,events:events[0:10]}'
aws ecs describe-task-definition --task-definition $ecsTaskDefinition --query 'taskDefinition.containerDefinitions[].{name:name,essential:essential,health:healthCheck,dependsOn:dependsOn,startTimeout:startTimeout,stopTimeout:stopTimeout}'
aws ecs describe-tasks --cluster $ecsCluster --tasks $ecsTaskArn --query 'tasks[].{createdAt:createdAt,pullStartedAt:pullStartedAt,pullStoppedAt:pullStoppedAt,startedAt:startedAt,health:healthStatus,stoppedReason:stoppedReason,containers:containers[].{name:name,last:lastStatus,health:healthStatus,reason:reason,exitCode:exitCode}}'
aws elbv2 describe-target-groups --target-group-arns $targetGroupArn
aws elbv2 describe-target-group-attributes --target-group-arn $targetGroupArn
aws elbv2 describe-target-health --target-group-arn $targetGroupArn'''

def task_fragment(p):
    containers=[]
    for name,sp,interval,timeout,command,dep in [
        ("adot",p["a_sp"],5,3,["CMD","/healthcheck"],"なし"),
        ("cwagent",p["c_sp"],10,5,["CMD","/opt/health/cwagent-process-check"],"なし"),
        ("backend",p["b_sp"],p["b_i"],p["b_t"],["CMD","/opt/health/backend-healthcheck"],p["b_dep"]),
        ("frontend",p["f_sp"],10,5,["CMD","/opt/health/frontend-healthcheck"],p["f_dep"])]:
        item=dict(name=name,essential=True,healthCheck=dict(command=command,interval=interval,timeout=timeout,retries=3,startPeriod=sp))
        if dep!="なし":
            dependency,condition=dep.split(" / ")
            item["dependsOn"]=[dict(containerName=dependency,condition=condition)]
        if name=="adot" and p["mode"]!="parallel":
            item["startTimeout"]=120
        if name=="backend" and p["mode"]=="serial":
            item["startTimeout"]=120
        containers.append(item)
    return {"containerDefinitions":containers}

SERVICE_FRAGMENT = {"healthCheckGracePeriodSeconds":360,"deploymentConfiguration":{"minimumHealthyPercent":100,"maximumPercent":200}}
ALB_FRAGMENT = {"TargetType":"ip","Protocol":"HTTP","Port":8080,"HealthCheckProtocol":"HTTP","HealthCheckPort":"traffic-port","HealthCheckPath":"/readyz","HealthCheckIntervalSeconds":10,"HealthCheckTimeoutSeconds":5,"HealthyThresholdCount":2,"UnhealthyThresholdCount":3,"Matcher":{"HttpCode":"200"}}

CONFIG_NOTES = [
    ["断片の扱い", "タスク例は既存の各containerDefinitionに同名でマージする検討用断片。image、CPU/メモリ、roles、portMappings、secrets、logs等を省略している。", "このJSONだけをregister-task-definitionへ渡さない。現在の完全な定義に、必要なフィールドだけを反映する。", "前提"],
    ["プローブの実体", "backend-healthcheckとfrontend-healthcheckは下記の自作スクリプト例。cwagent-process-checkは自作の静的実行ファイル等を同梱する設計契約。", "これらはAWS標準の実在コマンドではない。CWの実装は/proc内の実行ファイル・状態を厳密確認し、成功0／不在・異常1とする。", "設計 S23"],
    ["CW専用プローブ契約", "自コンテナ内の/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent本体を/proc/PID/exe等で識別し、生存・非ゾンビを確認。2秒以内に終了する小さな静的バイナリ等を事前に作る。", "この資料はそのバイナリをビルド・同梱していない。現行の実行可能なプロセス確認がある場合はそのコマンドを保持し、数値だけ比較する。", "設計"],
    ["LinuxとWindows", "以下のshはLinuxコンテナ内で動く例。作業PCのPowerShellで直接実行するコマンドではない。", "読み取り用AWS CLI例だけはPowerShell表記。シェルがないアプリイメージでは、アプリ内プローブや静的バイナリへ置き換える。", "前提"],
    ["ALB用の前提", "サンプルのフロントはHTTP8080、/readyz新設を仮定。既存のTLSやポート設定を変更してよいという意味ではない。", "既存HTTPSならProtocol/HealthCheckProtocol/Portを実環境に合わせる。フロントの/readyzは自分とバックの両方を検査する。", "設計"],
    ["Terraform例", "container_definitions = jsonencode([{ name = \"backend\", dependsOn = [{ containerName = \"adot\", condition = \"HEALTHY\" }] }]) のように、JSON構造内へ書く。", "説明用の短縮例で必須のimage等は省略。aws_ecs_serviceではhealth_check_grace_period_seconds=360。コンテナJSONにdepends_onを書かない。", "S26 S42 S43"],
    ["CloudFormation例", "コンテナ内のHealthCheck.StartPeriod=210、DependsOn=[{ContainerName: adot, Condition: HEALTHY}]。サービスのHealthCheckGracePeriodSeconds=360。", "リソース外側のDependsOnとは別。コンテナ内のStartTimeout=120は待たれるADOTに置く。", "S27 S28 S44"],
    ["P4の断片を省く", "P4はFargate依存時間を満たさないため、投入用と誤解されるタスクJSONを出力しない。値と不成立理由は比較表に記載。", "P0/P1/P2/P3/P5/P6の6断片を設定例に掲載。P3も条件付きであり、160秒保護を満たすものではない。", "設計"],
]
