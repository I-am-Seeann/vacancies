from datetime import datetime, timedelta

usernames = [
        'nino_beridze',
        'giorgi_kapanadze',
        'mariam_japaridze',
        'luka_tsiklauri',
        'ana_gogoladze',
        'davit_chkheidze',
        'sofia_kvaratskhelia',
        'nikoloz_bolkvadze',
        'ketevan_mchedlidze',
        'tornike_gelashvili',
        'natia_shubladze',
        'levan_kakhaberidze',
        'tamuna_kipshidze',
        'zurab_jishkariani',
        'eka_tsereteli'
    ]

job_data = [
    # IT Jobs
    (
        'Backend Developer',
        'Build robust server-side applications and APIs for our growing platform.',
        '''We are looking for a skilled Backend Developer to join our engineering team.

**Responsibilities:**
- Design and develop scalable server-side applications
- Create and maintain RESTful APIs
- Optimize database performance and queries
- Implement security and data protection
- Collaborate with frontend developers

**Requirements:**
- 2+ years experience with Python/Node.js/Java
- Strong knowledge of database systems (SQL/NoSQL)
- Experience with cloud platforms (AWS/Azure/GCP)
- Understanding of microservices architecture
- Bachelor's degree in Computer Science or related field

**We offer competitive salary, flexible hours, and professional development opportunities.''',
        'it',
        'TechCorp',
        '$85,000-$110,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=5)
    ),
    (
        'Full Stack Developer',
        'End-to-end web development from frontend UI to backend systems and databases.',
        '''Join us as a Full Stack Developer to work on exciting projects across our entire tech stack.

**Responsibilities:**
- Develop both frontend and backend components
- Create responsive web interfaces
- Build and maintain database schemas
- Implement user authentication and authorization
- Deploy and monitor applications

**Requirements:**
- Proficiency in JavaScript/TypeScript and Python
- Experience with React/Vue/Angular frameworks
- Knowledge of database design and optimization
- Familiarity with version control (Git)
- Strong problem-solving skills

**Perfect role for developers who enjoy working on diverse technical challenges.''',
        'it',
        'WebSolutions',
        '$90,000-$120,000',
        'Remote',
        datetime.utcnow() - timedelta(days=12)
    ),
    (
        'Data Scientist',
        'Extract insights from complex datasets to drive business decisions and strategy.',
        '''We seek a Data Scientist to transform raw data into actionable business intelligence.

**Responsibilities:**
- Analyze large, complex datasets to identify trends
- Build predictive models and machine learning algorithms
- Create data visualizations and dashboards
- Collaborate with business teams to define metrics
- Develop and maintain data pipelines

**Requirements:**
- Advanced degree in Statistics, Mathematics, or related field
- Proficiency in Python/R and SQL
- Experience with machine learning frameworks
- Strong statistical analysis background
- Excellent communication skills

**Work with cutting-edge technologies in a data-driven organization.''',
        'it',
        'DataDrive',
        '$95,000-$130,000',
        'Batumi',
        datetime.utcnow() - timedelta(days=8)
    ),
    (
        'DevOps Engineer',
        'Streamline development processes and maintain cloud infrastructure for optimal performance.',
        '''Looking for a DevOps Engineer to optimize our development pipeline and cloud infrastructure.

**Responsibilities:**
- Implement and maintain CI/CD pipelines
- Manage cloud infrastructure (AWS/Azure/GCP)
- Automate deployment and monitoring processes
- Ensure system reliability and performance
- Collaborate with development teams

**Requirements:**
- Experience with Docker and Kubernetes
- Proficiency in infrastructure as code (Terraform/CloudFormation)
- Knowledge of monitoring tools (Prometheus, Grafana)
- Strong scripting skills (Bash, Python)
- Understanding of networking and security

**Join our team to build scalable and reliable systems.''',
        'it',
        'CloudSystems',
        '$100,000-$140,000',
        'Hybrid',
        datetime.utcnow() - timedelta(days=15)
    ),
    (
        'QA Engineer',
        'Ensure software quality through comprehensive testing and automation frameworks.',
        '''We need a meticulous QA Engineer to maintain our high standards of software quality.

**Responsibilities:**
- Develop and execute test plans and test cases
- Create and maintain automated test scripts
- Perform manual and regression testing
- Identify, document, and track software defects
- Collaborate with developers to resolve issues

**Requirements:**
- Experience with test automation frameworks (Selenium, Cypress)
- Knowledge of software QA methodologies and tools
- Understanding of Agile/Scrum development processes
- Attention to detail and analytical thinking
- Strong communication skills

**Help us deliver bug-free software to our customers.''',
        'it',
        'SoftWorks',
        '$70,000-$95,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=20)
    ),

    # Design Jobs
    (
        'UI/UX Designer',
        'Create intuitive and visually appealing user interfaces for web and mobile applications.',
        '''Join our design team as a UI/UX Designer to create exceptional user experiences.

**Responsibilities:**
- Design user interfaces for web and mobile applications
- Create wireframes, prototypes, and mockups
- Conduct user research and usability testing
- Collaborate with product managers and developers
- Maintain design systems and style guides

**Requirements:**
- Portfolio demonstrating UI/UX design work
- Proficiency in design tools (Figma, Sketch, Adobe XD)
- Understanding of user-centered design principles
- Knowledge of responsive design principles
- Excellent visual design skills

**Create beautiful and functional designs that users love.''',
        'design',
        'DigitalCraft',
        '$65,000-$90,000',
        'Remote',
        datetime.utcnow() - timedelta(days=7)
    ),
    (
        'Graphic Designer',
        'Develop compelling visual content for branding, marketing, and digital platforms.',
        '''We're looking for a creative Graphic Designer to produce stunning visual content.

**Responsibilities:**
- Create marketing materials and brand assets
- Design social media graphics and advertisements
- Develop print and digital collateral
- Maintain brand consistency across all materials
- Collaborate with marketing team on campaigns

**Requirements:**
- Strong portfolio of graphic design work
- Proficiency in Adobe Creative Suite
- Understanding of typography and color theory
- Knowledge of print and digital production
- Creative thinking and attention to detail

**Bring your creative vision to our brand and marketing efforts.''',
        'design',
        'PixelPerfect',
        '$55,000-$75,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=18)
    ),
    (
        'Product Designer',
        'Shape product experiences from concept to launch through user-centered design.',
        '''Join us as a Product Designer to lead the design of our core products and features.

**Responsibilities:**
- Lead end-to-end product design process
- Conduct user research and gather insights
- Create user flows, wireframes, and high-fidelity designs
- Prototype and test design concepts
- Collaborate with engineering and product teams

**Requirements:**
- 3+ years of product design experience
- Strong portfolio of product design work
- Proficiency in design and prototyping tools
- Experience with design systems
- Excellent communication and presentation skills

**Help shape the future of our products through thoughtful design.''',
        'design',
        'InnovateLabs',
        '$80,000-$110,000',
        'Hybrid',
        datetime.utcnow() - timedelta(days=10)
    ),
    (
        'Web Designer',
        'Design and build engaging, responsive websites that provide excellent user experiences.',
        '''We need a Web Designer to create visually stunning and functional websites.

**Responsibilities:**
- Design and build responsive websites
- Create website layouts and user interfaces
- Optimize web pages for maximum speed and scalability
- Collaborate with developers on implementation
- Maintain and update existing websites

**Requirements:**
- Proficiency in HTML, CSS, and JavaScript
- Experience with responsive design principles
- Knowledge of web design trends and best practices
- Familiarity with CMS platforms
- Strong visual design skills

**Create web experiences that engage and convert visitors.''',
        'design',
        'AppFactory',
        '$60,000-$85,000',
        'Remote',
        datetime.utcnow() - timedelta(days=25)
    ),
    (
        'Motion Graphics Designer',
        'Create dynamic animations and visual effects for video content and digital platforms.',
        '''Looking for a Motion Graphics Designer to bring stories to life through animation.

**Responsibilities:**
- Create motion graphics for video content
- Design animated sequences for digital platforms
- Develop visual effects and transitions
- Collaborate with video producers and editors
- Animate logos and brand elements

**Requirements:**
- Proficiency in After Effects and other animation tools
- Strong understanding of timing and storytelling
- Knowledge of video editing principles
- Creative problem-solving skills
- Portfolio demonstrating motion graphics work

**Use animation to create engaging and memorable visual content.''',
        'design',
        'LogicLabs',
        '$70,000-$95,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=14)
    ),

    # Marketing Jobs
    (
        'Marketing Specialist',
        'Execute marketing campaigns across multiple channels to drive brand awareness and growth.',
        '''Join our marketing team as a Specialist to help execute our marketing strategy.

**Responsibilities:**
- Implement marketing campaigns across channels
- Create and distribute marketing materials
- Analyze campaign performance and ROI
- Coordinate with external agencies and partners
- Support event planning and execution

**Requirements:**
- 2+ years of marketing experience
- Knowledge of digital marketing channels
- Strong written and verbal communication skills
- Analytical thinking and attention to detail
- Bachelor's degree in Marketing or related field

**Gain experience across all aspects of modern marketing.''',
        'marketing',
        'FutureTech',
        '$50,000-$70,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=6)
    ),
    (
        'Digital Marketing Manager',
        'Lead digital strategy and campaigns to drive online presence and customer acquisition.',
        '''We seek a Digital Marketing Manager to lead our online marketing efforts.

**Responsibilities:**
- Develop and execute digital marketing strategy
- Manage SEO, SEM, and social media campaigns
- Analyze digital marketing metrics and KPIs
- Manage digital marketing budget
- Lead and mentor marketing team members

**Requirements:**
- 5+ years of digital marketing experience
- Proven track record of successful campaigns
- Expertise in Google Analytics and advertising platforms
- Strong leadership and project management skills
- Data-driven decision-making approach

**Lead our digital transformation and drive online growth.''',
        'marketing',
        'SmartDev',
        '$75,000-$100,000',
        'Hybrid',
        datetime.utcnow() - timedelta(days=22)
    ),
    (
        'Content Marketing Strategist',
        'Develop content strategy that engages audiences and supports business objectives.',
        '''Join us as a Content Marketing Strategist to shape our content vision and execution.

**Responsibilities:**
- Develop comprehensive content strategy
- Create content calendar and editorial plan
- Produce high-quality written and visual content
- Measure and optimize content performance
- Collaborate with subject matter experts

**Requirements:**
- 3+ years of content marketing experience
- Excellent writing and editing skills
- Knowledge of SEO and content optimization
- Experience with content management systems
- Strategic thinking and creativity

**Tell our brand story through compelling content.''',
        'marketing',
        'ByteSize',
        '$65,000-$85,000',
        'Remote',
        datetime.utcnow() - timedelta(days=9)
    ),
    (
        'SEO Specialist',
        'Optimize website content and structure to improve search engine rankings and organic traffic.',
        '''We need an SEO Specialist to drive organic growth through search engine optimization.

**Responsibilities:**
- Conduct keyword research and analysis
- Optimize website content and metadata
- Perform technical SEO audits and fixes
- Build and execute link building strategies
- Monitor and report on SEO performance

**Requirements:**
- 2+ years of SEO experience
- Proficiency with SEO tools (Ahrefs, SEMrush, Google Search Console)
- Understanding of technical SEO factors
- Knowledge of HTML and website structure
- Analytical mindset with attention to detail

**Help us dominate search results and drive organic traffic.''',
        'marketing',
        'NetSolutions',
        '$55,000-$75,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=16)
    ),
    (
        'Social Media Manager',
        'Manage social media presence and engage with communities across multiple platforms.',
        '''Looking for a Social Media Manager to grow our brand presence and engagement.

**Responsibilities:**
- Develop and execute social media strategy
- Create and schedule social media content
- Engage with followers and manage community
- Analyze social media metrics and insights
- Manage social media advertising campaigns

**Requirements:**
- 3+ years of social media management experience
- Proficiency with social media management tools
- Excellent written communication skills
- Knowledge of social media advertising
- Creative thinking and trend awareness

**Build and nurture our online community across social platforms.''',
        'marketing',
        'CodeMasters',
        '$60,000-$80,000',
        'Remote',
        datetime.utcnow() - timedelta(days=11)
    ),

    # Sales Jobs
    (
        'Sales Manager',
        'Lead sales team to achieve revenue targets and drive business growth.',
        '''We're hiring a Sales Manager to lead our sales team and drive revenue growth.

**Responsibilities:**
- Lead and mentor sales team members
- Develop and implement sales strategies
- Set sales targets and monitor performance
- Build relationships with key accounts
- Analyze sales data and market trends

**Requirements:**
- 5+ years of sales experience, 2+ in management
- Proven track record of meeting sales targets
- Strong leadership and coaching skills
- Excellent negotiation and communication skills
- Bachelor's degree in Business or related field

**Lead our sales team to new heights of success.''',
        'sales',
        'TechCorp',
        '$90,000-$120,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=4)
    ),
    (
        'Account Executive',
        'Manage client relationships and close deals to drive revenue and business growth.',
        '''Join our sales team as an Account Executive to build relationships and close deals.

**Responsibilities:**
- Identify and pursue new business opportunities
- Manage full sales cycle from prospecting to close
- Build and maintain client relationships
- Prepare and present proposals and contracts
- Achieve sales targets and quotas

**Requirements:**
- 3+ years of B2B sales experience
- Proven track record of meeting sales quotas
- Excellent communication and presentation skills
- Strong negotiation and closing skills
- Self-motivated and results-driven

**Help us grow our business through strategic sales.''',
        'sales',
        'WebSolutions',
        '$80,000-$110,000',
        'Batumi',
        datetime.utcnow() - timedelta(days=19)
    ),
    (
        'Business Development Representative',
        'Generate leads and identify new business opportunities through proactive outreach.',
        '''We need a Business Development Representative to fuel our sales pipeline.

**Responsibilities:**
- Generate qualified leads through outreach
- Conduct market research and identify prospects
- Schedule meetings and demos for sales team
- Maintain CRM database and track activities
- Collaborate with marketing on lead generation

**Requirements:**
- 1+ years of sales or business development experience
- Excellent communication and interpersonal skills
- Persistence and resilience in outreach
- Familiarity with CRM systems
- Goal-oriented and self-motivated

**Start your sales career and build the foundation for success.''',
        'sales',
        'DataDrive',
        '$45,000-$65,000',
        'Remote',
        datetime.utcnow() - timedelta(days=13)
    ),
    (
        'Sales Development Representative',
        'Qualify leads and set up sales opportunities for the account executive team.',
        '''Join us as a Sales Development Representative to drive our outbound sales efforts.

**Responsibilities:**
- Conduct outbound prospecting and cold calling
- Qualify inbound leads and schedule meetings
- Research target accounts and decision makers
- Maintain accurate records in CRM
- Achieve monthly meeting and lead quotas

**Requirements:**
- Excellent verbal and written communication skills
- Strong phone presence and confidence
- Ability to handle rejection and stay motivated
- Basic understanding of sales processes
- Ambitious and eager to learn

**Perfect entry-level role to launch your sales career.''',
        'sales',
        'CloudSystems',
        '$40,000-$55,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=21)
    ),
    (
        'Account Manager',
        'Nurture client relationships and ensure customer satisfaction and retention.',
        '''We're looking for an Account Manager to maintain and grow our client relationships.

**Responsibilities:**
- Manage portfolio of existing client accounts
- Ensure client satisfaction and retention
- Identify upsell and cross-sell opportunities
- Serve as main point of contact for clients
- Collaborate with internal teams on client needs

**Requirements:**
- 3+ years of account management experience
- Excellent relationship-building skills
- Strong problem-solving abilities
- Experience with CRM systems
- Customer-focused mindset

**Build lasting relationships and ensure client success.''',
        'sales',
        'SoftWorks',
        '$70,000-$95,000',
        'Hybrid',
        datetime.utcnow() - timedelta(days=17)
    ),

    # Other Jobs
    (
        'Project Coordinator',
        'Coordinate project activities and ensure timely delivery of project milestones.',
        '''Join our team as a Project Coordinator to support successful project execution.

**Responsibilities:**
- Coordinate project activities and timelines
- Schedule meetings and maintain project documentation
- Track project progress and report on milestones
- Facilitate communication between team members
- Assist with resource allocation and planning

**Requirements:**
- 2+ years of project coordination experience
- Excellent organizational and time management skills
- Strong written and verbal communication
- Proficiency with project management tools
- Attention to detail and problem-solving skills

**Keep our projects organized and on track.''',
        'other',
        'DigitalCraft',
        '$50,000-$70,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=3)
    ),
    (
        'Product Manager',
        'Define product vision and strategy, working with teams to bring products to market.',
        '''We seek a Product Manager to lead product development from concept to launch.

**Responsibilities:**
- Define product vision and roadmap
- Gather and prioritize product requirements
- Work with engineering and design teams on execution
- Analyze market trends and customer needs
- Define and track product success metrics

**Requirements:**
- 5+ years of product management experience
- Strong analytical and strategic thinking skills
- Excellent communication and leadership abilities
- Experience with Agile development methodologies
- Technical background or understanding

**Shape the future of our products and drive innovation.''',
        'other',
        'InnovateLabs',
        '$100,000-$140,000',
        'Hybrid',
        datetime.utcnow() - timedelta(days=23)
    ),
    (
        'Office Administrator',
        'Manage office operations and provide administrative support to ensure smooth daily functioning.',
        '''Looking for an Office Administrator to keep our office running efficiently.

**Responsibilities:**
- Manage office supplies and equipment
- Coordinate meetings and events
- Handle incoming calls and correspondence
- Maintain office records and documentation
- Support HR with onboarding and administrative tasks

**Requirements:**
- 2+ years of office administration experience
- Excellent organizational and multitasking skills
- Proficiency with office software and equipment
- Strong communication and interpersonal skills
- Professional demeanor and customer service orientation

**Be the backbone of our office operations.''',
        'other',
        'PixelPerfect',
        '$35,000-$50,000',
        'Tbilisi',
        datetime.utcnow() - timedelta(days=26)
    ),
    (
        'Human Resources Specialist',
        'Support HR functions including recruitment, employee relations, and policy implementation.',
        '''Join our HR team as a Specialist to support our growing organization.

**Responsibilities:**
- Manage recruitment and hiring processes
- Conduct employee onboarding and orientation
- Handle employee relations and inquiries
- Maintain HR records and documentation
- Assist with performance management processes

**Requirements:**
- 3+ years of HR experience
- Knowledge of HR laws and regulations
- Excellent interpersonal and communication skills
- Discretion and confidentiality
- Bachelor's degree in HR or related field

**Help us build and maintain a great workplace culture.''',
        'other',
        'LogicLabs',
        '$55,000-$75,000',
        'Batumi',
        datetime.utcnow() - timedelta(days=24)
    ),
    (
        'Customer Support Representative',
        'Provide excellent customer service and support to ensure customer satisfaction.',
        '''We need a Customer Support Representative to deliver exceptional service to our customers.

**Responsibilities:**
- Respond to customer inquiries via phone, email, and chat
- Troubleshoot and resolve customer issues
- Document customer interactions and feedback
- Escalate complex issues to appropriate teams
- Maintain product knowledge and expertise

**Requirements:**
- Excellent communication and problem-solving skills
- Customer-focused attitude and patience
- Ability to handle difficult situations professionally
- Basic technical aptitude
- High school diploma or equivalent

**Be the friendly voice that helps our customers succeed.''',
        'other',
        'FutureTech',
        '$30,000-$45,000',
        'Remote',
        datetime.utcnow() - timedelta(days=27)
    )
]