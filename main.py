import sys
import json
import time
import random
import base64
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem,
    QStackedWidget, QFrame, QDialog, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt, QSize, QSettings
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap, QPainter, QColor, QShortcut, QKeySequence

# -----------------------------------------------------------------------------
#  RESOURCES & ICONS (Base64 encoded to be self-contained)
# -----------------------------------------------------------------------------
# Using Fluent UI System Icons (https://github.com/microsoft/fluentui-system-icons)
# Converted to Base64 to avoid external file dependencies.
ICON_DATA = {
    "flag_light": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACLSURBVEhL7dOxDQAhEATR5whO4iRO4kQcIztJqGDBm0lC/5vlvQ+8BIg/SoDd23GAwz4s2LAc2HED2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LKDAd2FAN2HAO2HAM2HAM2HAO3HAG3HAE23AEm3AIlX/x/wE0iTCMg/woA/lADhF58EDgAAAABJRU5ErkJggg==",
    "flag_dark": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACQSURBVEhL7dOxDYAwEATR5wQO4iSO4iQcIztJKEHBD2+SoP/N8j54CRB/lAC7t+MANjws2LAc2XAD2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LID2LKDAd2FAN2HAO2HAM2HAM2HAO3HAG3HAE23AEm3AIlX/x/wE0gnC8g/woA/lMDnJtFDAAAAAElFTkSuQmCC",
    "flag_filled_light": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABTSURBVEhL7cwxAQAACASg+U+d3sCgISi5I4QqlSot24kDDuwwgA0PChbUZYAFDTjggAMOOOCAAw444IADDjjggAMOOOCAAw444IAD/g1wAcoMAE4f/5z3AAAAAElFTkSuQmCC",
    "flag_filled_dark": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABYSURBVEhL7cwxAQAACASg+U+d3sCgIZhckUIVS5Xm7SScYcALAzg8KVhwFwcsNOCA5QY44IADDjjggAMOOOCAAw444IADDjjggAMOOOCAA/4NcAEsMAE1vP9fzwAAAABJRU5ErkJggg==",
    "theme_light": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADISURBVEhL7dYxCsJgEAXgw6hdp5eRC1h7A7uDo5u4g7uDk7iCg3gCV3fwZk1WUnAQGg/8YVjyL/8lM2iUDkYAEVgIBeCCrA0wQdkBplVtQJsS2ANkQYy4l/sA1T9sDkKzY2sBXkCPAFKkHhJ0TUEB4AzQBVZAN8BfAE2wTQE2aA8QdEcLqAGeAF2wQXYBHAE3wToF2KANQNEcLagBeAI0wTYZAJwBVsE3A2wThsAcCUXfAAnAAzyH4u4APAzwAzgDXQ2k/wAAAABJRU5ErkJggg==",
    "theme_dark": "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADvSURBVEhL7dZBaoRAEAXgJ9E7Ozu9jFzE2hvsHYa7uJ27uI27uIODYALPYO/gzaokp+AgNN4b+GFY8i//pcwwA0kAEVgIBeCCrA0wQdkBplVtQJsS2ANkQYy4l/uAlv7ZHITmxtYCvIBuACpSjwg6p6CAA+AQUAU2wR3AF0ATbBNgQ/sAEddDAQfAIaAKbII7gC+AJtgmQIb2AyLu6wD2SLeCrgA0wTYZAJwBVsE3A2wThsAcCUUvAHGAg3gPx90B+DjAD+AMtDaq/8sBTG8AAbTeAVLYA7S+A1bwBch7gBwYx/iA85kXfgFdB3wDk4EAAAAASUVORK5CYII=",
}


def get_icon(name):
    """Decodes a Base64 string and returns a QIcon."""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(ICON_DATA[name]))
    return QIcon(pixmap)


# -----------------------------------------------------------------------------
#  QUESTION BANK (Full 50-question bank should be placed here)
# -----------------------------------------------------------------------------
QUESTION_BANK = {
    "Cloud Concepts": [
        {"q": "Which cloud model provides the highest degree of ownership and control?",
         "o": ["Public Cloud", "Private Cloud", "Hybrid Cloud", "Multi-cloud"], "a": "Private Cloud"},
        {"q": "What is the primary advantage of a consumption-based pricing model in the cloud?",
         "o": ["All services are free", "You only pay for what you use", "A single, fixed monthly bill", "Hardware costs are included"],
         "a": "You only pay for what you use"},
        {"q": "A platform as a service (PaaS) solution provides full control of the operating system that hosts the application.",
         "o": ["Yes", "No"], "a": "No"},
        {"q": "A platform as a service (PaaS) solution can automatically scale the number of application instances.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "Which cloud benefit refers to paying only for what you use?",
         "o": ["Consumption‑based model", "Economies of scale", "Capital expenditure", "Elasticity"],
         "a": "Consumption‑based model"},
        {"q": "Which deployment model gives shared access to resources across multiple organisations?",
         "o": ["Community Cloud", "Public Cloud", "Private Cloud", "Hybrid Cloud"], "a": "Community Cloud"},
        {"q": "Using subscription‑based cloud services is an example of which cost model?",
         "o": ["OpEx", "CapEx", "Fixed cost model", "Leasing model"], "a": "OpEx"},
        {"q": "Multiple customers securely sharing the same physical resources is called…",
         "o": ["Multi‑tenancy", "Single‑tenancy", "Virtualisation", "Dedicated hosting"], "a": "Multi‑tenancy"},
        {"q": "Reduced cost per unit due to provider scale is known as…",
         "o": ["Economies of scale", "Pay‑as‑you‑go", "Agility", "CapEx reduction"], "a": "Economies of scale"},
        {"q": "Which attribute ensures services remain available despite failures?",
         "o": ["Resiliency", "Agility", "Scalability", "Governance"], "a": "Resiliency"},
        {"q": "Which cloud model delivers complete applications over the Internet?",
         "o": ["SaaS", "PaaS", "IaaS", "On‑premises hosting"], "a": "SaaS"},
        {"q": "Adding more identical VM instances to meet demand is called…",
         "o": ["Horizontal scaling", "Vertical scaling", "Overclocking", "Edge scaling"], "a": "Horizontal scaling"}
    ],
    "Core Azure Services": [
        {"q": "Which Azure service is a serverless compute service that allows you to run code on-demand without managing infrastructure?",
         "o": ["Azure App Service", "Azure Virtual Machines", "Azure Functions", "Azure Kubernetes Service (AKS)"], "a": "Azure Functions"},
        {"q": "Which Azure storage service provides unlimited unstructured data storage?",
         "o": ["Azure Blob Storage", "Azure File Storage", "Azure Disks", "Azure SQL Database"], "a": "Azure Blob Storage"},
        {"q": "Which service provides fully managed VMs?",
         "o": ["Azure Virtual Machines", "Azure App Service", "Azure Container Instances", "Azure Batch"], "a": "Azure Virtual Machines"},
        {"q": "Which service hosts web apps and APIs without you managing infrastructure?",
         "o": ["Azure App Service", "Azure Virtual Machines", "Azure Functions", "Azure Container Instances"], "a": "Azure App Service"},
        {"q": "Globally distributed NoSQL database with multiple consistency models?",
         "o": ["Azure Cosmos DB", "Azure SQL Database", "Azure Database for PostgreSQL", "Azure Cache for Redis"], "a": "Azure Cosmos DB"},
        {"q": "Which service orchestrates containers using Kubernetes?",
         "o": ["Azure Kubernetes Service", "Azure Container Instances", "Azure Service Fabric", "VM Scale Sets"], "a": "Azure Kubernetes Service"},
        {"q": "Which service builds code‑free ETL pipelines?",
         "o": ["Azure Data Factory", "Azure Databricks", "Azure Synapse Analytics", "Azure HDInsight"], "a": "Azure Data Factory"},
        {"q": "Azure Stream Analytics is primarily used for…",
         "o": ["Real‑time data stream processing", "Batch ETL jobs", "Data cataloguing", "Blob lifecycle management"], "a": "Real‑time data stream processing"},
        {"q": "Service delivering virtual desktops in Azure?",
         "o": ["Azure Virtual Desktop", "Azure VMware Solution", "Azure DevTest Labs", "Windows 365"], "a": "Azure Virtual Desktop"},
        {"q": "Messaging service ingesting millions of events per second?",
         "o": ["Azure Event Hubs", "Azure Service Bus", "Azure Queue Storage", "Azure Notification Hubs"], "a": "Azure Event Hubs"},
        {"q": "Which service sends cross‑platform push notifications to mobile devices?",
         "o": ["Azure Notification Hubs", "Azure Event Grid", "Azure IoT Hub", "Azure SignalR Service"], "a": "Azure Notification Hubs"}
    ],
    "Security & Compliance": [
        {"q": "Azure Active Directory (Entra ID) manages identities and access to Azure resources.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "To implement Azure multifactor authentication you must sync on‑premises identities to the cloud.",
         "o": ["Yes", "No"], "a": "No"},
        {"q": "Azure MFA can be required for both administrative and non‑administrative user accounts.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "Which Azure service is Microsoft’s cloud‑native SIEM/SOAR?",
         "o": ["Microsoft Sentinel", "Microsoft Defender for Cloud", "Azure Monitor", "Splunk Cloud"], "a": "Microsoft Sentinel"},
        {"q": "Central view of security posture with recommendations?",
         "o": ["Microsoft Defender for Cloud", "Azure Advisor", "Azure Monitor", "Azure Security Benchmark"], "a": "Microsoft Defender for Cloud"},
        {"q": "Network Security Groups filter traffic at which OSI layers?",
         "o": ["Layer 3 and 4", "Layer 7", "Layer 2", "Layer 5"], "a": "Layer 3 and 4"},
        {"q": "Azure DDoS Protection Standard includes a cost‑protection guarantee.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "Governance service that enforces compliance rules on Azure resources?",
         "o": ["Azure Policy", "Azure Blueprints", "Management Groups", "Azure RBAC"], "a": "Azure Policy"},
        {"q": "Which feature prevents accidental deletion or modification of resources?",
         "o": ["Resource Locks", "Azure RBAC", "Management Groups", "Activity Log"], "a": "Resource Locks"},
        {"q": "You need to collect and automatically analyse security events from Azure AD.  Which service should you use?",
         "o": ["Azure Synapse Analytics", "Azure Key Vault", "Azure Sentinel", "Azure AD Connect"], "a": "Azure Sentinel"}
    ],
    "Pricing & Support": [
        {"q": "All Azure services in public preview are excluded from service‑level agreements (SLAs).",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "Tool that helps estimate total cost of ownership when migrating to Azure:",
         "o": ["Azure TCO Calculator", "Azure Pricing Calculator", "Azure Cost Management", "Azure Migrate"], "a": "Azure TCO Calculator"},
        {"q": "Purchasing option offering up to 72 % savings for 1‑ or 3‑year commitment:",
         "o": ["Azure Reserved Instances", "Azure Spot VMs", "Azure Hybrid Benefit", "Pay‑as‑you‑go"], "a": "Azure Reserved Instances"},
        {"q": "Which Azure support plan is included free of charge with every subscription?",
         "o": ["Basic", "Developer", "Standard", "Professional Direct"], "a": "Basic"},
        {"q": "Calculator used to estimate the monthly cost of a specific Azure architecture:",
         "o": ["Azure Pricing Calculator", "Azure TCO Calculator", "Azure Advisor", "Azure Cost Analysis"], "a": "Azure Pricing Calculator"},
        {"q": "Azure Budgets can trigger alerts when forecast or actual spend exceeds thresholds.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "Applying existing Windows Server licences to Azure VMs is enabled by…",
         "o": ["Azure Hybrid Benefit", "License Mobility", "Dev/Test subscription", "Reserved Capacity"], "a": "Azure Hybrid Benefit"},
        {"q": "Typical financially‑backed SLA for most regional Azure services:",
         "o": ["99.9 %", "95 %", "99.99 %", "100 %"], "a": "99.9 %"},
        {"q": "Feature that recommends right‑sizing under‑utilised resources:",
         "o": ["Azure Advisor Cost recommendations", "Azure Cost Management alerts", "Budget Alerts", "Azure Migrate"], "a": "Azure Advisor Cost recommendations"},
        {"q": "Support plan offering a 15‑minute initial response for critical issues:",
         "o": ["Professional Direct", "Standard", "Developer", "Basic"], "a": "Professional Direct"}
    ],
    "Azure Architecture and Services": [
        {"q": "What is the primary purpose of an Azure Region Pair?",
         "o": ["To provide lower latency for all users", "To offer data residency and disaster recovery capabilities",
               "To connect two different virtual networks", "To reduce the cost of data transfer"],
         "a": "To offer data residency and disaster recovery capabilities"},
        {"q": "Physically separate datacentres within an Azure region are called…",
         "o": ["Availability Zones", "Availability Sets", "Region Pairs", "Fault Domains"], "a": "Availability Zones"},
        {"q": "Azure Load Balancer operates at which OSI layer?",
         "o": ["Layer 4", "Layer 7", "Layer 3", "Layer 2"], "a": "Layer 4"},
        {"q": "Azure Application Gateway operates at which OSI layer?",
         "o": ["Layer 7", "Layer 4", "Layer 3", "Layer 2"], "a": "Layer 7"},
        {"q": "Azure Resource Manager (ARM) templates are expressed in which format?",
         "o": ["JSON", "YAML", "XML", "HCL"], "a": "JSON"},
        {"q": "Service that replicates VMs to another region for disaster recovery:",
         "o": ["Azure Site Recovery", "Azure Backup", "Azure Traffic Manager", "VM Scale Sets"], "a": "Azure Site Recovery"},
        {"q": "DNS‑based global traffic‑routing service:",
         "o": ["Azure Traffic Manager", "Azure Front Door", "Azure Load Balancer", "Azure CDN"], "a": "Azure Traffic Manager"},
        {"q": "Azure Monitor logs (queried with Kusto) are stored in a…",
         "o": ["Log Analytics Workspace", "Storage Account", "Application Insights", "Event Hub"], "a": "Log Analytics Workspace"},
        {"q": "Service accelerating delivery of static content via edge locations:",
         "o": ["Azure CDN", "Azure Front Door", "ExpressRoute", "Azure Bastion"], "a": "Azure CDN"},
        {"q": "Azure Advisor provides guidance across cost, performance, reliability, operations, and security.",
         "o": ["Yes", "No"], "a": "Yes"},
        {"q": "A canary deployment gradually directs a small percentage of user traffic to a new version.",
         "o": ["Yes", "No"], "a": "Yes"}
    ]
}

EXAM_MINUTES = 60
PASS_SCORE = 700
MAX_SCORE = 1000

# -----------------------------------------------------------------------------
#  STYLESHEETS (QSS) - Based on Fluent UI
# -----------------------------------------------------------------------------
STYLES = {
    "light": {
        "bg": "#f5f5f5", "bg_alt": "#ffffff", "text": "#202020",
        "primary": "#0078D4", "primary_text": "#ffffff", "border": "#e0e0e0",
        "answered": "#e1f5fe", "flagged": "#fff9c4", "unanswered": "#f5f5f5",
        "pass": "#107C10", "fail": "#A4262C"
    },
    "dark": {
        "bg": "#252525", "bg_alt": "#323232", "text": "#ffffff",
        "primary": "#2899f5", "primary_text": "#000000", "border": "#4a4a4a",
        "answered": "#023e8a", "flagged": "#6c5800", "unanswered": "#404040",
        "pass": "#6BCB77", "fail": "#D23F3F"
    }
}


def get_stylesheet(theme):
    """Generates the QSS stylesheet for the given theme (light/dark)."""
    s = STYLES[theme]
    return f"""
        /* General */
        QWidget {{
            background-color: {s['bg']};
            color: {s['text']};
            font-family: 'Segoe UI', 'Roboto', 'sans-serif';
        }}
        QMainWindow {{ background-color: {s['bg']}; }}

        /* Top Bar */
        #TopBar {{
            background-color: {s['bg_alt']};
            border-bottom: 1px solid {s['border']};
        }}
        #ExamTitle {{ font-size: 15px; font-weight: 600; padding-left: 10px; }}
        #TimerLabel {{ font-size: 22px; font-weight: 600; }}

        /* Question Palette */
        #QuestionPalette {{
            border: none;
            border-right: 1px solid {s['border']};
            background-color: {s['bg_alt']};
        }}
        QListWidget::item {{
            font-size: 15px;
            padding: 12px;
            border-radius: 4px;
            margin: 2px 8px;
            border: 1px solid transparent; /* for alignment */
        }}
        QListWidget::item:hover {{
            background-color: {s['border']};
        }}
        QListWidget::item:selected {{
            background-color: {s['primary']};
            color: {s['primary_text']};
            font-weight: 600;
        }}

        /* Question Area */
        #QuestionLabel {{ font-size: 18px; padding-bottom: 15px; line-height: 1.5; }}
        QRadioButton {{ font-size: 16px; padding: 10px 0; }}
        QRadioButton::indicator {{ width: 18px; height: 18px; }}

        /* Bottom Bar */
        #BottomBar {{
            background-color: {s['bg_alt']};
            border-top: 1px solid {s['border']};
            padding: 10px 20px;
        }}
        QPushButton {{
            font-size: 15px;
            font-weight: 600;
            padding: 10px 25px;
            min-height: 44px;
            min-width: 120px;
            border-radius: 4px;
            border: 1px solid {s['border']};
            background-color: {s['bg_alt']};
            color: {s['text']};
        }}
        QPushButton:hover {{
            border-color: {s['primary']};
            color: {s['primary']};
        }}
        QPushButton#NextButton, QPushButton#SubmitButton {{
            background-color: {s['primary']};
            color: {s['primary_text']};
            border-color: {s['primary']};
        }}
        QPushButton#NextButton:hover, QPushButton#SubmitButton:hover {{
            background-color: #005a9e;
        }}
        #FlagButton {{
            border: none;
            background-color: transparent;
            min-width: 44px;
        }}
        #FlagButton:hover {{
            background-color: {s['border']};
        }}

        /* Review Screen */
        #ReviewList::item {{ padding: 10px; }}
        #ReviewItemWidget {{
            border: 1px solid {s['border']};
            border-radius: 4px;
            padding: 10px;
        }}
        #ReviewList QLabel {{ font-size: 16px; }}
        #SummaryBar {{ padding: 10px; border-bottom: 1px solid {s['border']}; }}
        #SummaryBar QLabel {{
            font-size: 14px;
            font-weight: 600;
            padding: 8px;
            border-radius: 4px;
        }}
    """


# -----------------------------------------------------------------------------
#  MAIN APPLICATION
# -----------------------------------------------------------------------------
class ExamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OnVUE Exam Simulator | AZ-900: Microsoft Azure Fundamentals")
        self.setGeometry(100, 100, 1440, 810)

        self.settings = QSettings("PearsonVUE_Simulator", "ExamApp")
        self.questions = self._load_questions()
        self.responses, self.flags = {}, set()
        self.current_index = 0
        self.start_time = 0
        self.current_theme = self.settings.value("theme", "light", type=str)

        self._init_ui()
        self._setup_shortcuts()
        self.stacked_widget.setCurrentWidget(self.startup_screen)

    def _init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self._create_startup_screen()
        self._create_exam_screen()
        self._create_review_screen()
        self._create_results_screen()

        self.stacked_widget.addWidget(self.startup_screen)
        self.stacked_widget.addWidget(self.exam_screen)
        self.stacked_widget.addWidget(self.review_screen)
        self.stacked_widget.addWidget(self.results_screen)

        self._apply_theme()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+D"), self, self._toggle_theme)
        QShortcut(QKeySequence(Qt.Key.Key_F), self, self._toggle_flag)
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self._prev_question)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self._next_question)

    def _load_questions(self):
        all_q = [(domain, q_data) for domain, q_list in QUESTION_BANK.items() for q_data in q_list]
        random.shuffle(all_q)
        return all_q

    # --- UI Creation Methods ---

    def _create_startup_screen(self):
        self.startup_screen = QWidget()
        layout = QVBoxLayout(self.startup_screen)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("AZ-900: Microsoft Azure Fundamentals")
        title.setStyleSheet("font-size: 32px; font-weight: 600; margin-bottom: 20px;")

        start_button = QPushButton("Start Exam")
        start_button.setObjectName("NextButton")
        start_button.setFixedSize(200, 60)
        start_button.clicked.connect(self._start_exam)

        layout.addWidget(title)
        layout.addWidget(start_button)

    def _create_exam_screen(self):
        self.exam_screen = QWidget()
        main_layout = QVBoxLayout(self.exam_screen)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._create_top_bar(main_layout)
        self._create_exam_body(main_layout)

    def _create_top_bar(self, parent_layout):
        top_bar = QWidget(objectName="TopBar")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)

        self.exam_title = QLabel("AZ-900: Microsoft Azure Fundamentals")
        self.exam_title.setObjectName("ExamTitle")

        self.timer_label = QLabel("60:00")
        self.timer_label.setObjectName("TimerLabel")

        self.theme_button = QPushButton()
        self.theme_button.setObjectName("FlagButton")
        self.theme_button.setFixedSize(44, 44)
        self.theme_button.clicked.connect(self._toggle_theme)

        top_bar_layout.addWidget(self.exam_title)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.timer_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.theme_button)

        parent_layout.addWidget(top_bar)

    def _create_exam_body(self, parent_layout):
        body_layout = QHBoxLayout()
        body_layout.setSpacing(0)

        self.palette = QListWidget(objectName="QuestionPalette")
        self.palette.setFixedWidth(120)
        self.palette.setIconSize(QSize(16, 16))
        self.palette.currentRowChanged.connect(self._jump_to_question)
        for i in range(len(self.questions)):
            item = QListWidgetItem(f"Question {i + 1}")
            self.palette.addItem(item)
        body_layout.addWidget(self.palette)

        main_content = QFrame()
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(40, 30, 40, 0)

        self.question_label = QLabel(objectName="QuestionLabel")
        self.question_label.setWordWrap(True)

        self.option_group = QButtonGroup(self)
        self.option_widgets = [QRadioButton() for _ in range(4)]
        options_container = QVBoxLayout()
        options_container.setSpacing(10)
        for i, rb in enumerate(self.option_widgets):
            self.option_group.addButton(rb, i)
            options_container.addWidget(rb)

        main_content_layout.addWidget(self.question_label, 1)
        main_content_layout.addLayout(options_container, 2)

        bottom_bar = self._create_bottom_bar()
        main_content_layout.addWidget(bottom_bar)

        body_layout.addWidget(main_content, 1)
        parent_layout.addLayout(body_layout, 1)

    def _create_bottom_bar(self):
        bottom_bar = QWidget(objectName="BottomBar")
        bottom_layout = QHBoxLayout(bottom_bar)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self._prev_question)

        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("NextButton")
        self.next_button.clicked.connect(self._next_question)

        self.flag_button = QPushButton()
        self.flag_button.setObjectName("FlagButton")
        self.flag_button.clicked.connect(self._toggle_flag)

        bottom_layout.addWidget(self.prev_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.flag_button)
        bottom_layout.addWidget(self.next_button)
        return bottom_bar

    def _create_review_screen(self):
        self.review_screen = QWidget()
        layout = QVBoxLayout(self.review_screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        summary_bar = QWidget(objectName="SummaryBar")
        summary_layout = QHBoxLayout(summary_bar)
        self.summary_answered = QLabel()
        self.summary_unanswered = QLabel()
        self.summary_flagged = QLabel()
        summary_layout.addStretch()
        summary_layout.addWidget(self.summary_answered)
        summary_layout.addWidget(self.summary_unanswered)
        summary_layout.addWidget(self.summary_flagged)
        summary_layout.addStretch()

        self.review_list = QListWidget(objectName="ReviewList")

        review_nav = QWidget(objectName="BottomBar")
        review_nav_layout = QHBoxLayout(review_nav)
        edit_button = QPushButton("Go to Question")
        edit_button.clicked.connect(self._edit_from_review)
        submit_button = QPushButton("Finish Exam")
        submit_button.setObjectName("SubmitButton")
        submit_button.clicked.connect(self._confirm_submit)

        review_nav_layout.addStretch()
        review_nav_layout.addWidget(edit_button)
        review_nav_layout.addWidget(submit_button)

        layout.addWidget(summary_bar)
        layout.addWidget(self.review_list, 1)
        layout.addWidget(review_nav)

    def _create_results_screen(self):
        self.results_screen = QWidget()
        layout = QVBoxLayout(self.results_screen)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.verdict_label = QLabel()
        self.verdict_label.setStyleSheet("font-size: 60px; font-weight: 800;")
        self.score_label = QLabel()
        self.score_label.setStyleSheet("font-size: 28px;")
        self.pass_info_label = QLabel(f"(Required score to pass: {PASS_SCORE})")
        self.pass_info_label.setStyleSheet("font-size: 16px; color: #888;")

        self.score_visual = QFrame()
        self.score_visual.setFixedSize(400, 30)
        self.score_visual.setStyleSheet("border-radius: 15px;")
        self.score_bar = QFrame(self.score_visual)
        self.score_bar.setStyleSheet("border-radius: 14px;")

        close_button = QPushButton("Close")
        close_button.setObjectName("NextButton")
        close_button.setFixedSize(200, 60)
        close_button.clicked.connect(self.close)

        layout.addWidget(self.verdict_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pass_info_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_visual, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(40)
        layout.addWidget(close_button, 0, Qt.AlignmentFlag.AlignCenter)

    # --- Core Logic Methods ---

    def _start_exam(self):
        self.start_time = time.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.timer.start(1000)
        self._load_question()
        self.stacked_widget.setCurrentWidget(self.exam_screen)

    def _load_question(self):
        _, q_data = self.questions[self.current_index]
        q_text = f"<b>Question {self.current_index + 1} of {len(self.questions)}</b><br/><br/>{q_data['q']}"
        self.question_label.setText(q_text)

        options = q_data['o'][:]
        random.shuffle(options)

        self.option_group.setExclusive(False)
        for i, rb in enumerate(self.option_widgets):
            rb.setChecked(False)
            if i < len(options):
                rb.setText(options[i]);
                rb.show()
            else:
                rb.hide()
        self.option_group.setExclusive(True)

        if self.current_index in self.responses:
            for rb in self.option_widgets:
                if rb.text() == self.responses[self.current_index]:
                    rb.setChecked(True);
                    break

        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setText("Next" if self.current_index < len(self.questions) - 1 else "Review")
        self.palette.setCurrentRow(self.current_index)
        self._update_palette()

    def _save_answer(self):
        if btn := self.option_group.checkedButton():
            self.responses[self.current_index] = btn.text()
        self._update_palette()

    def _next_question(self):
        self._save_answer()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self._load_question()
        else:
            self._show_review_screen()

    def _prev_question(self):
        self._save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self._load_question()

    def _jump_to_question(self, row):
        if row != -1 and row != self.current_index:
            self._save_answer()
            self.current_index = row
            self._load_question()

    def _toggle_flag(self):
        if self.current_index in self.flags:
            self.flags.discard(self.current_index)
        else:
            self.flags.add(self.current_index)
        self._update_palette()

    def _update_palette(self):
        theme = STYLES[self.current_theme]
        icon_suffix = "dark" if self.current_theme == "dark" else "light"
        self.flag_button.setIcon(
            get_icon(f'flag_filled_{icon_suffix}' if self.current_index in self.flags else f'flag_{icon_suffix}'))

        for i in range(self.palette.count()):
            item = self.palette.item(i)
            color = theme['unanswered']
            icon = QIcon()
            if i in self.flags:
                color = theme['flagged'];
                icon = get_icon(f'flag_filled_{icon_suffix}')
            elif i in self.responses:
                color = theme['answered']
            item.setBackground(QColor(color))
            item.setIcon(icon)

    def _update_timer(self):
        remaining = (EXAM_MINUTES * 60) - (time.time() - self.start_time)
        if remaining <= 0:
            self.timer.stop()
            self._auto_submit()
            return

        if remaining < 300 and int(remaining) % 2 == 0:  # Flash red in last 5 mins
            self.timer_label.setStyleSheet(
                f"color: {STYLES[self.current_theme]['fail']}; font-size: 22px; font-weight: 600;")
        else:
            self.timer_label.setStyleSheet(
                f"color: {STYLES[self.current_theme]['text']}; font-size: 22px; font-weight: 600;")

        self.timer_label.setText(f"{int(remaining // 60):02d}:{int(remaining % 60):02d}")

    def _toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.settings.setValue("theme", self.current_theme)
        self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(get_stylesheet(self.current_theme))
        self.theme_button.setIcon(get_icon(f'theme_{self.current_theme}'))
        self._update_palette()

    def _show_review_screen(self):
        self.review_list.clear()
        s = STYLES[self.current_theme]

        self.summary_answered.setText(
            f"<span style='background-color:{s['answered']}; padding:4px;'>&nbsp;✅ Answered: {len(self.responses)}&nbsp;</span>"
        )
        self.summary_unanswered.setText(
            f"<span style='background-color:{s['unanswered']}; padding:4px;'>&nbsp;❌ Unanswered: {len(self.questions) - len(self.responses)}&nbsp;</span>"
        )
        self.summary_flagged.setText(
            f"<span style='background-color:{s['flagged']}; padding:4px;'>&nbsp;⚠️ Flagged: {len(self.flags)}&nbsp;</span>"
        )

        self.review_list.setSpacing(10)

        for i, (_, q_data) in enumerate(self.questions):
            widget = QWidget(objectName="ReviewItemWidget")
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(6)

            q_label = QLabel()
            q_label.setTextFormat(Qt.TextFormat.RichText)
            q_label.setWordWrap(True)
            q_label.setStyleSheet("font-size: 16px; font-weight: 500;")
            flagged_tag = " <span style='color:orange'>(🚩 Flagged)</span>" if i in self.flags else ""
            q_label.setText(f"<b>Q{i + 1}:</b> {q_data['q']}{flagged_tag}")

            a_label = QLabel()
            a_label.setTextFormat(Qt.TextFormat.RichText)
            a_label.setWordWrap(True)
            a_label.setStyleSheet("font-size: 15px;")
            response = self.responses.get(i, "<i>Not Answered</i>")
            a_label.setText(f"<b>Your Answer:</b> {response}")

            layout.addWidget(q_label)
            layout.addWidget(a_label)

            widget.setLayout(layout)
            widget.adjustSize()

            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.review_list.addItem(item)
            self.review_list.setItemWidget(item, widget)

        self.stacked_widget.setCurrentWidget(self.review_screen)

    def _edit_from_review(self):
        if not self.review_list.selectedItems(): return
        self.current_index = self.review_list.currentRow()
        self._load_question()
        self.stacked_widget.setCurrentWidget(self.exam_screen)

    def _confirm_submit(self):
        unanswered = len(self.questions) - len(self.responses)
        msg = "Are you sure you want to finish the exam?" + (
            f"\n\nYou have {unanswered} unanswered question(s)." if unanswered > 0 else "")
        if QMessageBox.question(self, "Finish Exam", msg,
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self._calculate_and_show_results()

    def _auto_submit(self):
        QMessageBox.information(self, "Time's Up!", "The exam time has expired. Your exam will now be submitted.")
        self._calculate_and_show_results()

    def _calculate_and_show_results(self):
        self._save_answer()
        correct = sum(1 for i, (_, q) in enumerate(self.questions) if self.responses.get(i) == q['a'])
        score = int((correct / len(self.questions)) * MAX_SCORE)
        passed = score >= PASS_SCORE

        self.verdict_label.setText("PASS" if passed else "FAIL")
        s = STYLES[self.current_theme]
        verdict_color = s['pass'] if passed else s['fail']
        self.verdict_label.setStyleSheet(f"font-size: 60px; font-weight: 800; color: {verdict_color};")
        self.score_label.setText(f"Score: {score} / {MAX_SCORE}")

        self.score_visual.setStyleSheet(f"background-color: {s['border']}; border-radius: 15px;")
        bar_width = int((score / MAX_SCORE) * self.score_visual.width())
        self.score_bar.setGeometry(1, 1, bar_width - 2, self.score_visual.height() - 2)
        self.score_bar.setStyleSheet(f"background-color: {verdict_color}; border-radius: 14px;")

        self.stacked_widget.setCurrentWidget(self.results_screen)

    def closeEvent(self, event):
        if self.stacked_widget.currentWidget() in [self.exam_screen, self.review_screen]:
            if QMessageBox.question(self, 'Exit Exam', 'Are you sure you want to exit? Your progress will be lost.',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# -----------------------------------------------------------------------------
#  MAIN EXECUTION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # On Windows, 'Segoe UI' is usually available. For other OSs, Qt will
    # fall back to a font like 'Roboto' or a default sans-serif.
    # QFontDatabase.addApplicationFont("path/to/segoeui.ttf")

    win = ExamApp()
    win.show()
    sys.exit(app.exec())