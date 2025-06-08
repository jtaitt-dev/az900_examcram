import sys, time, random, logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem, QStackedWidget, QFrame, QMessageBox
from PyQt6.QtCore import QTimer, Qt, QSize, QSettings
from PyQt6.QtGui import QFontDatabase, QIcon, QPixmap, QPainter, QColor, QPainterPath, QPen, QShortcut, QKeySequence

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(message)s')

QUESTION_BANK = {  # full 54‑question bank
    "Cloud Concepts": [
        {"q": "Which cloud model provides the highest degree of ownership and control?",
         "o": ["Public Cloud", "Private Cloud", "Hybrid Cloud", "Multi-cloud"],
         "a": "Private Cloud",
         "exp": "A private cloud is dedicated to a single organization—no shared tenancy—so you control hardware, networking, security, and compliance end‑to‑end."},
        {"q": "What is the primary advantage of a consumption-based pricing model in the cloud?",
         "o": ["All services are free", "You only pay for what you use",
               "A single, fixed monthly bill", "Hardware costs are included"],
         "a": "You only pay for what you use",
         "exp": "Cloud meters CPU, storage, and bandwidth per second/GB. Unused capacity isn’t billed, turning fixed CapEx into elastic OpEx."},
        {"q": "A platform as a service (PaaS) solution provides full control of the operating system that hosts the application.",
         "o": ["Yes", "No"], "a": "No",
         "exp": "In PaaS, OS patching, scaling, and middleware are abstracted away; you deploy code only. Full OS control is IaaS territory."},
        {"q": "A platform as a service (PaaS) solution can automatically scale the number of application instances.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Auto‑scale rules (e.g., in Azure App Service) spin instances up/down on CPU/throughput thresholds—zero manual VM babysitting."},
        {"q": "Which cloud benefit refers to paying only for what you use?",
         "o": ["Consumption‑based model", "Economies of scale", "Capital expenditure", "Elasticity"],
         "a": "Consumption‑based model",
         "exp": "Consumption‑based = utility billing. You’re charged for exact resource minutes/GBs, eliminating idle over‑provisioning costs."},
        {"q": "Which deployment model gives shared access to resources across multiple organisations?",
         "o": ["Community Cloud", "Public Cloud", "Private Cloud", "Hybrid Cloud"],
         "a": "Community Cloud",
         "exp": "Community clouds pool infrastructure for orgs with common concerns (e.g., healthcare, government) while keeping others out."},
        {"q": "Using subscription‑based cloud services is an example of which cost model?",
         "o": ["OpEx", "CapEx", "Fixed cost model", "Leasing model"],
         "a": "OpEx",
         "exp": "Cloud shifts spend to operating expense—recurring, usage‑based—versus upfront capital expenditure on hardware/software."},
        {"q": "Multiple customers securely sharing the same physical resources is called…",
         "o": ["Multi‑tenancy", "Single‑tenancy", "Virtualisation", "Dedicated hosting"],
         "a": "Multi‑tenancy",
         "exp": "Tenant isolation is logical; hypervisors/container runtimes slice hardware so many customers run side‑by‑side cost‑effectively."},
        {"q": "Reduced cost per unit due to provider scale is known as…",
         "o": ["Economies of scale", "Pay‑as‑you‑go", "Agility", "CapEx reduction"],
         "a": "Economies of scale",
         "exp": "Hyperscalers buy hardware/power in bulk; savings are passed on, lowering per‑VM/GB price compared to on‑prem procurement."},
        {"q": "Which attribute ensures services remain available despite failures?",
         "o": ["Resiliency", "Agility", "Scalability", "Governance"],
         "a": "Resiliency",
         "exp": "Resilient architectures add redundancy, failover, and self‑healing so workloads survive hardware, zone, or regional outages."},
        {"q": "Which cloud model delivers complete applications over the Internet?",
         "o": ["SaaS", "PaaS", "IaaS", "On‑premises hosting"],
         "a": "SaaS",
         "exp": "SaaS = finished product (e.g., Microsoft 365). Vendor handles everything from datacenter to updates—users just consume the app."},
        {"q": "Adding more identical VM instances to meet demand is called…",
         "o": ["Horizontal scaling", "Vertical scaling", "Overclocking", "Edge scaling"],
         "a": "Horizontal scaling",
         "exp": "Horizontal (scale‑out) adds nodes; vertical (scale‑up) adds CPU/RAM to one node. Cloud prefers horizontal for fault isolation."}
    ],
    "Core Azure Services": [
        {"q": "Which Azure service is a serverless compute service that allows you to run code on-demand without managing infrastructure?",
         "o": ["Azure App Service", "Azure Virtual Machines", "Azure Functions", "Azure Kubernetes Service (AKS)"],
         "a": "Azure Functions",
         "exp": "Azure Functions executes event‑driven code; Microsoft provisions containers, scales to zero, and bills per millisecond."},
        {"q": "Which Azure storage service provides unlimited unstructured data storage?",
         "o": ["Azure Blob Storage", "Azure File Storage", "Azure Disks", "Azure SQL Database"],
         "a": "Azure Blob Storage",
         "exp": "Blob Storage is object storage: petabyte scale, flat namespace, lifecycle tiers (Hot/Cool/Archive), global replication options."},
        {"q": "Which service provides fully managed VMs?",
         "o": ["Azure Virtual Machines", "Azure App Service", "Azure Container Instances", "Azure Batch"],
         "a": "Azure Virtual Machines",
         "exp": "Azure VMs give you OS‑level access while Microsoft manages the physical hosts, networking, power, and rack hardware lifecycle."},
        {"q": "Which service hosts web apps and APIs without you managing infrastructure?",
         "o": ["Azure App Service", "Azure Virtual Machines", "Azure Functions", "Azure Container Instances"],
         "a": "Azure App Service",
         "exp": "App Service runs IIS/Linux containers behind the scenes; you push code or Docker images and get built‑in CI/CD, SSL, scaling."},
        {"q": "Globally distributed NoSQL database with multiple consistency models?",
         "o": ["Azure Cosmos DB", "Azure SQL Database", "Azure Database for PostgreSQL", "Azure Cache for Redis"],
         "a": "Azure Cosmos DB",
         "exp": "Cosmos DB offers turnkey global replication, <10 ms reads, and five tunable consistency levels (Strong→Eventual)."},
        {"q": "Which service orchestrates containers using Kubernetes?",
         "o": ["Azure Kubernetes Service", "Azure Container Instances", "Azure Service Fabric", "VM Scale Sets"],
         "a": "Azure Kubernetes Service",
         "exp": "AKS offloads control‑plane setup/patching so you focus on deploying pods; integrates with AAD, CI/CD, and autoscale."},
        {"q": "Which service builds code‑free ETL pipelines?",
         "o": ["Azure Data Factory", "Azure Databricks", "Azure Synapse Analytics", "Azure HDInsight"],
         "a": "Azure Data Factory",
         "exp": "ADF drag‑and‑drop pipelines move/transform data across 90+ connectors, scheduling, mapping data flows, and CI/CD."},
        {"q": "Azure Stream Analytics is primarily used for…",
         "o": ["Real‑time data stream processing", "Batch ETL jobs", "Data cataloguing", "Blob lifecycle management"],
         "a": "Real‑time data stream processing",
         "exp": "Stream Analytics uses SQL‑like queries to ingest telemetry/events from Event Hubs/IoT Hub, processing millions/sec with <1 sec latency."},
        {"q": "Service delivering virtual desktops in Azure?",
         "o": ["Azure Virtual Desktop", "Azure VMware Solution", "Azure DevTest Labs", "Windows 365"],
         "a": "Azure Virtual Desktop",
         "exp": "AVD streams Windows desktops/apps from Azure VMs, supporting FSLogix profiles, multi‑session, and AAD authentication."},
        {"q": "Messaging service ingesting millions of events per second?",
         "o": ["Azure Event Hubs", "Azure Service Bus", "Azure Queue Storage", "Azure Notification Hubs"],
         "a": "Azure Event Hubs",
         "exp": "Event Hubs partitions incoming event streams for parallel consumers—ideal for big‑data pipelines and real‑time analytics."},
        {"q": "Which service sends cross‑platform push notifications to mobile devices?",
         "o": ["Azure Notification Hubs", "Azure Event Grid", "Azure IoT Hub", "Azure SignalR Service"],
         "a": "Azure Notification Hubs",
         "exp": "Notification Hubs abstracts APNS/FCM/WNS; you broadcast or tag‑target millions of devices with one REST call."}
    ],
    "Security & Compliance": [
        {"q": "Azure Active Directory (Entra ID) manages identities and access to Azure resources.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "AAD provides authentication, MFA, conditional access, and token issuance for Azure, M365, and custom apps."},
        {"q": "To implement Azure multifactor authentication you must sync on‑premises identities to the cloud.",
         "o": ["Yes", "No"], "a": "No",
         "exp": "You can enable cloud‑only users for Azure MFA; directory sync (Azure AD Connect) is optional, not mandatory."},
        {"q": "Azure MFA can be required for both administrative and non‑administrative user accounts.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Conditional Access policies let you enforce MFA on any role; best practice is MFA everywhere, especially privileged roles."},
        {"q": "Which Azure service is Microsoft’s cloud‑native SIEM/SOAR?",
         "o": ["Microsoft Sentinel", "Microsoft Defender for Cloud", "Azure Monitor", "Splunk Cloud"],
         "a": "Microsoft Sentinel",
         "exp": "Sentinel ingests logs, correlates incidents with KQL analytics, and automates response playbooks via Logic Apps."},
        {"q": "Central view of security posture with recommendations?",
         "o": ["Microsoft Defender for Cloud", "Azure Advisor", "Azure Monitor", "Azure Security Benchmark"],
         "a": "Microsoft Defender for Cloud",
         "exp": "Defender for Cloud scores resources against benchmarks, flags misconfigurations, and can auto‑enable protections."},
        {"q": "Network Security Groups filter traffic at which OSI layers?",
         "o": ["Layer 3 and 4", "Layer 7", "Layer 2", "Layer 5"],
         "a": "Layer 3 and 4",
         "exp": "NSGs evaluate source/destination IP, port, protocol—classic L3/L4 ACL, not HTTP headers or payload."},
        {"q": "Azure DDoS Protection Standard includes a cost‑protection guarantee.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "If a protected resource is hit and you incur scale‑out bandwidth costs, Microsoft reimburses under the SLA."},
        {"q": "Governance service that enforces compliance rules on Azure resources?",
         "o": ["Azure Policy", "Azure Blueprints", "Management Groups", "Azure RBAC"],
         "a": "Azure Policy",
         "exp": "Policy evaluates ARM requests and existing resources; deny or audit non‑compliant ones using JSON rule definitions."},
        {"q": "Which feature prevents accidental deletion or modification of resources?",
         "o": ["Resource Locks", "Azure RBAC", "Management Groups", "Activity Log"],
         "a": "Resource Locks",
         "exp": "Read‑Only or Delete locks override RBAC, forcing an explicit lock removal before changes—cheap safety net."},
        {"q": "You need to collect and automatically analyse security events from Azure AD.  Which service should you use?",
         "o": ["Azure Synapse Analytics", "Azure Key Vault", "Azure Sentinel", "Azure AD Connect"],
         "a": "Azure Sentinel",
         "exp": "Sentinel connectors stream Azure AD sign‑ins and audit logs into a Log Analytics workspace for rule‑based correlation."}
    ],
    "Pricing & Support": [
        {"q": "All Azure services in public preview are excluded from service‑level agreements (SLAs).",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Preview = beta; Microsoft provides no uptime guarantee until GA, so service credits don’t apply."},
        {"q": "Tool that helps estimate total cost of ownership when migrating to Azure:",
         "o": ["Azure TCO Calculator", "Azure Pricing Calculator", "Azure Cost Management", "Azure Migrate"],
         "a": "Azure TCO Calculator",
         "exp": "The TCO calculator compares on‑prem server depreciation, power, labor vs. equivalent Azure VM/SAN costs."},
        {"q": "Purchasing option offering up to 72 % savings for 1‑ or 3‑year commitment:",
         "o": ["Azure Reserved Instances", "Azure Spot VMs", "Azure Hybrid Benefit", "Pay‑as‑you‑go"],
         "a": "Azure Reserved Instances",
         "exp": "RIs trade flexibility for price: commit to baseline VM type/region for 1‑3 years; you still pay if unused."},
        {"q": "Which Azure support plan is included free of charge with every subscription?",
         "o": ["Basic", "Developer", "Standard", "Professional Direct"],
         "a": "Basic",
         "exp": "Basic offers 24×7 billing support, online docs, and community forums but no SLA for technical response."},
        {"q": "Calculator used to estimate the monthly cost of a specific Azure architecture:",
         "o": ["Azure Pricing Calculator", "Azure TCO Calculator", "Azure Advisor", "Azure Cost Analysis"],
         "a": "Azure Pricing Calculator",
         "exp": "Pricing Calculator models per‑service consumption—VM hours, storage GB, egress GB—to give a monthly forecast."},
        {"q": "Azure Budgets can trigger alerts when forecast or actual spend exceeds thresholds.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Budgets integrate with Cost Management and Action Groups; they email/trigger automation at 80/100% etc."},
        {"q": "Applying existing Windows Server licences to Azure VMs is enabled by…",
         "o": ["Azure Hybrid Benefit", "License Mobility", "Dev/Test subscription", "Reserved Capacity"],
         "a": "Azure Hybrid Benefit",
         "exp": "Hybrid Benefit lets you BYOL for Windows Server/SQL, reducing per‑hour VM cost—requires Software Assurance."},
        {"q": "Typical financially‑backed SLA for most regional Azure services:",
         "o": ["99.9 %", "95 %", "99.99 %", "100 %"],
         "a": "99.9 %",
         "exp": "Regional PaaS services (e.g., Storage) guarantee 99.9% uptime; Zonal services often raise to 99.99%."},
        {"q": "Feature that recommends right‑sizing under‑utilised resources:",
         "o": ["Azure Advisor Cost recommendations", "Azure Cost Management alerts", "Budget Alerts", "Azure Migrate"],
         "a": "Azure Advisor Cost recommendations",
         "exp": "Advisor analyses metrics and flags VMs at <5% CPU or over‑provisioned disks, suggesting cheaper SKUs."},
        {"q": "Support plan offering a 15‑minute initial response for critical issues:",
         "o": ["Professional Direct", "Standard", "Developer", "Basic"],
         "a": "Professional Direct",
         "exp": "ProDirect gives fastest SLA (15 min Sev‑A), TAM guidance, and proactive monitoring for production workloads."}
    ],
    "Azure Architecture and Services": [
        {"q": "What is the primary purpose of an Azure Region Pair?",
         "o": ["To provide lower latency for all users",
               "To offer data residency and disaster recovery capabilities",
               "To connect two different virtual networks",
               "To reduce the cost of data transfer"],
         "a": "To offer data residency and disaster recovery capabilities",
         "exp": "Each Azure region is paired with another 300+ km away; updates roll sequentially and you can design active‑passive DR."},
        {"q": "Physically separate datacentres within an Azure region are called…",
         "o": ["Availability Zones", "Availability Sets", "Region Pairs", "Fault Domains"],
         "a": "Availability Zones",
         "exp": "AZs give independent power, cooling, and network; deploying redundantly across 2‑3 AZs bumps SLA to 99.99%."},
        {"q": "Azure Load Balancer operates at which OSI layer?",
         "o": ["Layer 4", "Layer 7", "Layer 3", "Layer 2"],
         "a": "Layer 4",
         "exp": "Load Balancer is TCP/UDP passthrough with health probes—no HTTP header inspection (use Application Gateway for L7)."},
        {"q": "Azure Application Gateway operates at which OSI layer?",
         "o": ["Layer 7", "Layer 4", "Layer 3", "Layer 2"],
         "a": "Layer 7",
         "exp": "App Gateway terminates TLS, does URL‑based routing, WAF rules, session affinity—full HTTP(S) stack."},
        {"q": "Azure Resource Manager (ARM) templates are expressed in which format?",
         "o": ["JSON", "YAML", "XML", "HCL"],
         "a": "JSON",
         "exp": "Classic ARM exports/deployments are JSON. (Bicep is a transpiled DSL but still outputs JSON templates.)"},
        {"q": "Service that replicates VMs to another region for disaster recovery:",
         "o": ["Azure Site Recovery", "Azure Backup", "Azure Traffic Manager", "VM Scale Sets"],
         "a": "Azure Site Recovery",
         "exp": "ASR performs continuous replication; a failover boots VM disks in the target region with minimal RPO/RTO."},
        {"q": "DNS‑based global traffic‑routing service:",
         "o": ["Azure Traffic Manager", "Azure Front Door", "Azure Load Balancer", "Azure CDN"],
         "a": "Azure Traffic Manager",
         "exp": "Traffic Manager returns the best endpoint IP (Priority, Weighted, Performance, etc.) via authoritative DNS response."},
        {"q": "Azure Monitor logs (queried with Kusto) are stored in a…",
         "o": ["Log Analytics Workspace", "Storage Account", "Application Insights", "Event Hub"],
         "a": "Log Analytics Workspace",
         "exp": "Workspaces store compressed log tables; KQL queries power Monitor, Sentinel, and Advisor analytics."},
        {"q": "Service accelerating delivery of static content via edge locations:",
         "o": ["Azure CDN", "Azure Front Door", "ExpressRoute", "Azure Bastion"],
         "a": "Azure CDN",
         "exp": "Azure CDN caches blobs/web assets on POPs worldwide, cutting latency and offloading origin bandwidth."},
        {"q": "Azure Advisor provides guidance across cost, performance, reliability, operations, and security.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Advisor scans telemetry and surfaces actionable best‑practice recommendations across five well‑architected pillars."},
        {"q": "A canary deployment gradually directs a small percentage of user traffic to a new version.",
         "o": ["Yes", "No"], "a": "Yes",
         "exp": "Canary releases mitigate risk: 1‑5% traffic sees vNext; metrics are monitored before 100% rollout."}
    ]
}

STYLES = {
    "light": {"bg": "#f5f5f5", "bg_alt": "#ffffff", "text": "#202020", "primary": "#0078D4", "primary_text": "#ffffff", "border": "#e0e0e0", "answered": "#e1f5fe", "flagged": "#fff9c4", "unanswered": "#f5f5f5", "pass": "#107C10", "fail": "#A4262C"},
    "dark": {"bg": "#252525", "bg_alt": "#323232", "text": "#ffffff", "primary": "#2899f5", "primary_text": "#000000", "border": "#4a4a4a", "answered": "#023e8a", "flagged": "#6c5800", "unanswered": "#404040", "pass": "#6BCB77", "fail": "#D23F3F"}
}

def get_stylesheet(t):
    s = STYLES[t]
    return f"""QWidget{{background:{s['bg']};color:{s['text']};font-family:'Segoe UI','Roboto','sans-serif';}}QMainWindow{{background:{s['bg']};}}#TopBar{{background:{s['bg_alt']};border-bottom:1px solid {s['border']};}}#ExamTitle{{font-size:15px;font-weight:600;padding-left:10px;}}#TimerLabel{{font-size:22px;font-weight:600;}}#QuestionPalette{{border:none;border-right:1px solid {s['border']};background:{s['bg_alt']};}}QListWidget::item{{font-size:15px;padding:12px;border-radius:4px;margin:2px 8px;border:1px solid transparent;}}QListWidget::item:hover{{background:{s['border']};}}QListWidget::item:selected{{background:{s['primary']};color:{s['primary_text']};font-weight:600;}}#QuestionLabel{{font-size:18px;padding-bottom:15px;line-height:1.5;}}QRadioButton{{font-size:16px;padding:10px 0;}}QRadioButton::indicator{{width:18px;height:18px;}}#BottomBar{{background:{s['bg_alt']};border-top:1px solid {s['border']};padding:10px 20px;}}QPushButton{{font-size:15px;font-weight:600;padding:10px 25px;min-height:44px;min-width:120px;border-radius:4px;border:1px solid {s['border']};background:{s['bg_alt']};color:{s['text']};}}QPushButton:hover{{border-color:{s['primary']};color:{s['primary']};}}QPushButton#NextButton,QPushButton#SubmitButton{{background:{s['primary']};color:{s['primary_text']};border-color:{s['primary']};}}QPushButton#NextButton:hover,QPushButton#SubmitButton:hover{{background:#005a9e;}}#FlagButton{{border:none;background:transparent;min-width:44px;}}#FlagButton:hover{{background:{s['border']};}}#ReviewList::item{{padding:10px;}}#ReviewItemWidget{{border:1px solid {s['border']};border-radius:4px;padding:10px;}}#ReviewList QLabel{{font-size:16px;}}#SummaryBar{{padding:10px;border-bottom:1px solid {s['border']};}}#SummaryBar QLabel{{font-size:14px;font-weight:600;padding:8px;border-radius:4px;}}"""

def flag_icon(t, filled):
    c = QColor("#ffffff" if t == "dark" else "#202020")
    pm = QPixmap(24, 24); pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(c, 2)); p.drawLine(6, 4, 6, 20)
    if filled: p.setBrush(c)
    path = QPainterPath(); path.moveTo(6, 4); path.lineTo(18, 4); path.lineTo(12, 10); path.lineTo(18, 16); path.lineTo(6, 16)
    p.drawPath(path); p.end(); return QIcon(pm)

def theme_icon(t):
    c = QColor("#ffffff" if t == "dark" else "#202020")
    pm = QPixmap(24, 24); pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen); p.setBrush(c)
    if t == "light": p.drawEllipse(5, 4, 14, 14); p.setBrush(QColor("#00000000")); p.drawEllipse(10, 4, 14, 14)
    else: p.drawEllipse(6, 6, 12, 12)
    p.end(); return QIcon(pm)

EXAM_MINUTES, PASS_SCORE, MAX_SCORE = 60, 700, 1000

class ExamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OnVUE Exam Simulator | AZ-900: Microsoft Azure Fundamentals")
        self.setGeometry(100, 100, 1440, 810)
        self.settings = QSettings("PearsonVUE_Simulator", "ExamApp")
        self.questions = self._load_questions()
        self.responses, self.flags, self.current_index, self.start_time = {}, set(), 0, 0
        self.current_theme = self.settings.value("theme", "light", str)
        self.feedback_screen_created = False
        self._init_ui(); self._setup_shortcuts(); self.stacked_widget.setCurrentWidget(self.startup_screen)

    def _init_ui(self):
        self.stacked_widget = QStackedWidget(); self.setCentralWidget(self.stacked_widget)
        self._create_startup_screen(); self._create_exam_screen(); self._create_review_screen(); self._create_results_screen()
        self.stacked_widget.addWidget(self.startup_screen); self.stacked_widget.addWidget(self.exam_screen); self.stacked_widget.addWidget(self.review_screen); self.stacked_widget.addWidget(self.results_screen)
        self._apply_theme()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+D"), self, self._toggle_theme)
        QShortcut(QKeySequence(Qt.Key.Key_F), self, self._toggle_flag)
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self._prev_question)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self._next_question)

    def _load_questions(self):
        q = [(d, i) for d, l in QUESTION_BANK.items() for i in l]; random.shuffle(q); return q

    def _create_startup_screen(self):
        self.startup_screen = QWidget(); v = QVBoxLayout(self.startup_screen); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t = QLabel("AZ-900: Microsoft Azure Fundamentals"); t.setStyleSheet("font-size:32px;font-weight:600;margin-bottom:20px;")
        b = QPushButton("Start Exam"); b.setObjectName("NextButton"); b.setFixedSize(200, 60); b.clicked.connect(self._start_exam)
        v.addWidget(t); v.addWidget(b)

    def _create_exam_screen(self):
        self.exam_screen = QWidget(); v = QVBoxLayout(self.exam_screen); v.setContentsMargins(0,0,0,0); v.setSpacing(0)
        self._create_top_bar(v); self._create_exam_body(v)

    def _create_top_bar(self, pl):
        top = QWidget(objectName="TopBar"); h = QHBoxLayout(top); h.setContentsMargins(10,0,10,0)
        self.exam_title = QLabel("AZ-900: Microsoft Azure Fundamentals"); self.exam_title.setObjectName("ExamTitle")
        self.timer_label = QLabel("60:00"); self.timer_label.setObjectName("TimerLabel")
        self.theme_button = QPushButton(); self.theme_button.setObjectName("FlagButton"); self.theme_button.setFixedSize(44,44); self.theme_button.clicked.connect(self._toggle_theme)
        h.addWidget(self.exam_title); h.addStretch(); h.addWidget(self.timer_label); h.addStretch(); h.addWidget(self.theme_button); pl.addWidget(top)

    def _create_exam_body(self, pl):
        body = QHBoxLayout(); body.setSpacing(0)
        self.palette = QListWidget(objectName="QuestionPalette"); self.palette.setFixedWidth(120); self.palette.setIconSize(QSize(16,16)); self.palette.currentRowChanged.connect(self._jump_to_question)
        for i in range(len(self.questions)): self.palette.addItem(QListWidgetItem(f"Question {i+1}"))
        body.addWidget(self.palette)
        main = QFrame(); m = QVBoxLayout(main); m.setContentsMargins(40,30,40,0)
        self.question_label = QLabel(objectName="QuestionLabel"); self.question_label.setWordWrap(True)
        self.option_group = QButtonGroup(self); self.option_widgets = [QRadioButton() for _ in range(4)]
        o = QVBoxLayout(); o.setSpacing(10)
        for i, rb in enumerate(self.option_widgets): self.option_group.addButton(rb, i); o.addWidget(rb)
        m.addWidget(self.question_label,1); m.addLayout(o,2); m.addWidget(self._create_bottom_bar()); body.addWidget(main,1); pl.addLayout(body,1)

    def _create_bottom_bar(self):
        bar = QWidget(objectName="BottomBar"); h = QHBoxLayout(bar)
        self.prev_button = QPushButton("Previous"); self.prev_button.clicked.connect(self._prev_question)
        self.next_button = QPushButton("Next"); self.next_button.setObjectName("NextButton"); self.next_button.clicked.connect(self._next_question)
        self.flag_button = QPushButton(); self.flag_button.setObjectName("FlagButton"); self.flag_button.clicked.connect(self._toggle_flag); self.flag_button.setIcon(flag_icon(self.current_theme, False)); self.flag_button.setIconSize(QSize(20,20))
        h.addWidget(self.prev_button); h.addStretch(); h.addWidget(self.flag_button); h.addWidget(self.next_button); return bar

    def _create_review_screen(self):
        self.review_screen = QWidget(); v = QVBoxLayout(self.review_screen); v.setContentsMargins(0,0,0,0); v.setSpacing(0)
        sum_bar = QWidget(objectName="SummaryBar"); s = QHBoxLayout(sum_bar); self.summary_answered, self.summary_unanswered, self.summary_flagged = QLabel(), QLabel(), QLabel(); s.addStretch(); s.addWidget(self.summary_answered); s.addWidget(self.summary_unanswered); s.addWidget(self.summary_flagged); s.addStretch()
        self.review_list = QListWidget(objectName="ReviewList")
        nav = QWidget(objectName="BottomBar"); h = QHBoxLayout(nav); edit = QPushButton("Go to Question"); edit.clicked.connect(self._edit_from_review); sub = QPushButton("Finish Exam"); sub.setObjectName("SubmitButton"); sub.clicked.connect(self._confirm_submit); h.addStretch(); h.addWidget(edit); h.addWidget(sub)
        v.addWidget(sum_bar); v.addWidget(self.review_list,1); v.addWidget(nav)

    def _create_results_screen(self):
        self.results_screen = QWidget(); v = QVBoxLayout(self.results_screen); v.setAlignment(Qt.AlignmentFlag.AlignCenter); v.setSpacing(20)
        self.verdict_label, self.score_label = QLabel(), QLabel(); self.verdict_label.setStyleSheet("font-size:60px;font-weight:800;"); self.score_label.setStyleSheet("font-size:28px;")
        self.pass_info_label = QLabel(f"(Required score to pass: {PASS_SCORE})"); self.pass_info_label.setStyleSheet("font-size:16px;color:#888;")
        self.score_visual = QFrame(); self.score_visual.setFixedSize(400,30); self.score_visual.setStyleSheet("border-radius:15px;"); self.score_bar = QFrame(self.score_visual); self.score_bar.setStyleSheet("border-radius:14px;")
        close = QPushButton("Close"); close.setObjectName("NextButton"); close.setFixedSize(200,60); close.clicked.connect(self.close)
        v.addWidget(self.verdict_label,0,Qt.AlignmentFlag.AlignCenter); v.addWidget(self.score_label,0,Qt.AlignmentFlag.AlignCenter); v.addWidget(self.pass_info_label,0,Qt.AlignmentFlag.AlignCenter); v.addWidget(self.score_visual,0,Qt.AlignmentFlag.AlignCenter); v.addSpacing(40); v.addWidget(close,0,Qt.AlignmentFlag.AlignCenter)

    def _start_exam(self):
        logging.info("Exam started"); self.start_time = time.time(); self.timer = QTimer(self); self.timer.timeout.connect(self._update_timer); self.timer.start(1000); self._load_question(); self.stacked_widget.setCurrentWidget(self.exam_screen)

    def _load_question(self):
        _, q = self.questions[self.current_index]; self.question_label.setText(f"<b>Question {self.current_index+1} of {len(self.questions)}</b><br/><br/>{q['q']}")
        opts = q['o'][:]; random.shuffle(opts); self.option_group.setExclusive(False)
        for i, rb in enumerate(self.option_widgets):
            rb.setChecked(False)
            if i < len(opts): rb.setText(opts[i]); rb.show()
            else: rb.hide()
        self.option_group.setExclusive(True)
        if self.current_index in self.responses:
            for rb in self.option_widgets:
                if rb.text() == self.responses[self.current_index]: rb.setChecked(True); break
        self.prev_button.setEnabled(self.current_index>0); self.next_button.setText("Next" if self.current_index < len(self.questions)-1 else "Review"); self.palette.setCurrentRow(self.current_index); self._update_palette()

    def _save_answer(self):
        if (btn:=self.option_group.checkedButton()): self.responses[self.current_index]=btn.text(); logging.info(f"Save Q{self.current_index+1}:{btn.text()}"); self._update_palette()

    def _next_question(self): self._save_answer(); self.current_index = min(self.current_index+1, len(self.questions)-1); self._load_question() if self.current_index < len(self.questions)-1 else self._show_review_screen()
    def _prev_question(self): self._save_answer(); self.current_index = max(self.current_index-1,0); self._load_question()
    def _jump_to_question(self,row):
        if row!=-1 and row!=self.current_index: self._save_answer(); self.current_index=row; self._load_question()
    def _toggle_flag(self):
        if self.current_index in self.flags: self.flags.remove(self.current_index)
        else: self.flags.add(self.current_index)
        self._update_palette()

    def _update_palette(self):
        t=self.current_theme; self.flag_button.setIcon(flag_icon(t,self.current_index in self.flags))
        for i in range(self.palette.count()):
            item=self.palette.item(i); bg=STYLES[t]['unanswered']; icon=QIcon()
            if i in self.flags: bg=STYLES[t]['flagged']; icon=flag_icon(t,True)
            elif i in self.responses: bg=STYLES[t]['answered']
            item.setBackground(QColor(bg)); item.setIcon(icon)

    def _update_timer(self):
        rem=(EXAM_MINUTES*60)-(time.time()-self.start_time)
        if rem<=0: self.timer.stop(); self._auto_submit(); return
        color = STYLES[self.current_theme]['fail'] if rem<300 and int(rem)%2==0 else STYLES[self.current_theme]['text']
        self.timer_label.setStyleSheet(f"color:{color};font-size:22px;font-weight:600;")
        self.timer_label.setText(f"{int(rem//60):02d}:{int(rem%60):02d}")

    def _toggle_theme(self):
        self.current_theme="dark" if self.current_theme=="light" else "light"; self.settings.setValue("theme",self.current_theme); self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(get_stylesheet(self.current_theme)); self.theme_button.setIcon(theme_icon(self.current_theme)); self._update_palette()

    def _show_review_screen(self):
        self.review_list.clear()
        self.review_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)

        s = STYLES[self.current_theme]
        answered   = len(self.responses)
        unanswered = len(self.questions) - answered
        flagged    = len(self.flags)

        self.summary_answered.setText(
            f"<span style='background:{s['answered']};padding:4px;'>✅ Answered: {answered}</span>")
        self.summary_unanswered.setText(
            f"<span style='background:{s['unanswered']};padding:4px;'>❌ Unanswered: {unanswered}</span>")
        self.summary_flagged.setText(
            f"<span style='background:{s['flagged']};padding:4px;'>🚩 Flagged: {flagged}</span>")

        self.review_list.setSpacing(10)

        for i, (_, q) in enumerate(self.questions):
            widget = QWidget(objectName="ReviewItemWidget")
            vbox   = QVBoxLayout(widget)
            vbox.setContentsMargins(10, 10, 10, 10)
            vbox.setSpacing(6)

            flag_tag = " <span style='color:orange'>(🚩)</span>" if i in self.flags else ""
            vbox.addWidget(
                QLabel(f"<b>Q{i+1}:</b> {q['q']}{flag_tag}", wordWrap=True, styleSheet="font-size:16px;font-weight:500;")
            )
            vbox.addWidget(
                QLabel(f"<b>Your Answer:</b> {self.responses.get(i, '<i>Not Answered</i>')}", wordWrap=True,
                       styleSheet="font-size:15px;")
            )

            widget.adjustSize()                       # ensure correct height
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.review_list.addItem(item)
            self.review_list.setItemWidget(item, widget)

        self.stacked_widget.setCurrentWidget(self.review_screen)

    def _edit_from_review(self):
        if self.review_list.selectedItems(): self.current_index=self.review_list.currentRow(); self._load_question(); self.stacked_widget.setCurrentWidget(self.exam_screen)

    def _confirm_submit(self):
        un=len(self.questions)-len(self.responses)
        msg="Finish exam?"; msg+=f"\n\nYou have {un} unanswered question(s)." if un else ""
        if QMessageBox.question(self,"Finish Exam",msg,QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)==QMessageBox.StandardButton.Yes: self._calculate_and_show_results()

    def _auto_submit(self): QMessageBox.information(self,"Time's Up!","Submitting exam."); self._calculate_and_show_results()

    def _calculate_and_show_results(self):
        self._save_answer(); corr=sum(1 for i,(_,q) in enumerate(self.questions) if self.responses.get(i)==q['a'])
        score=int(corr/len(self.questions)*MAX_SCORE); passed=score>=PASS_SCORE; s=STYLES[self.current_theme]; clr=s['pass'] if passed else s['fail']
        self.verdict_label.setText("PASS" if passed else "FAIL"); self.verdict_label.setStyleSheet(f"font-size:60px;font-weight:800;color:{clr};")
        self.score_label.setText(f"Score: {score} / {MAX_SCORE}"); self.score_visual.setStyleSheet(f"background:{s['border']};border-radius:15px;")
        bw=int(score/MAX_SCORE*self.score_visual.width()); self.score_bar.setGeometry(1,1,bw-2,self.score_visual.height()-2); self.score_bar.setStyleSheet(f"background:{clr};border-radius:14px;")
        if not self.feedback_screen_created:
            self._create_feedback_screen(); fb=QPushButton("View Detailed Feedback"); fb.setObjectName("SubmitButton"); fb.setFixedSize(220,50); fb.clicked.connect(self._show_feedback_screen)
            self.results_screen.layout().addWidget(fb,0,Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.setCurrentWidget(self.results_screen)

    def _create_feedback_screen(self):
        self.feedback_screen = QWidget()
        layout = QVBoxLayout(self.feedback_screen)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.feedback_list = QListWidget()
        self.feedback_list.setSpacing(12)
        self.feedback_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)  # no blue highlight
        layout.addWidget(self.feedback_list)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("NextButton")
        close_btn.setFixedSize(200, 48)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.addWidget(self.feedback_screen)
        self.feedback_screen_created = True

    def _show_feedback_screen(self):
        self.feedback_list.clear()

        for i, (_, q) in enumerate(self.questions):
            widget = QWidget()
            vbox   = QVBoxLayout(widget)
            vbox.setContentsMargins(10, 10, 10, 10)
            vbox.setSpacing(6)

            vbox.addWidget(
                QLabel(f"<b>Q{i+1}:</b> {q['q']}", wordWrap=True,
                       styleSheet="font-size:16px;font-weight:600;")
            )

            user_answer = self.responses.get(i, "<i>Not Answered</i>")
            correct     = q['a']

            if user_answer == "<i>Not Answered</i>":
                result_text = f"❌ <b>Skipped.</b> Correct: <b>{correct}</b>"
            elif user_answer == correct:
                result_text = f"✅ <b>Correct.</b> You chose <b>{user_answer}</b>"
            else:
                result_text = f"❌ <b>Incorrect.</b> You chose <b>{user_answer}</b> | Correct: <b>{correct}</b>"

            vbox.addWidget(
                QLabel(result_text, wordWrap=True, styleSheet="font-size:15px;")
            )

            if exp := q.get('exp'):
                vbox.addWidget(
                    QLabel(f"<i>Explanation:</i> {exp}", wordWrap=True,
                           styleSheet="font-size:14px;color:#888;")
                )

            widget.adjustSize()                      # ensure correct height
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.feedback_list.addItem(item)
            self.feedback_list.setItemWidget(item, widget)

        self.stacked_widget.setCurrentWidget(self.feedback_screen)

    def closeEvent(self,e):
        if self.stacked_widget.currentWidget() in (self.exam_screen,self.review_screen):
            if QMessageBox.question(self,"Exit Exam","Exit and lose progress?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)==QMessageBox.StandardButton.Yes: e.accept()
            else: e.ignore()
        else: e.accept()

if __name__=="__main__":
    app=QApplication(sys.argv); QFontDatabase.addApplicationFont(":/fonts/"); win=ExamApp(); win.show(); sys.exit(app.exec())