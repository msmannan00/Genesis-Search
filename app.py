from django.utils.text import unescape_entities

from modules.user_data_parser.parse_instance.i_crawl_crawler.static_parse_controller import static_parse_controller
from modules.user_data_parser.parse_instance.local_shared_model.url_model import url_model


m_html = "&lt;head&gt; &lt;title&gt; Home - riseup.net &lt;/title&gt; &lt;meta content=&quot;width=device-width, initial-scale=1.0&quot; name=&quot;viewport&quot;&gt; &lt;meta charset=&quot;UTF-8&quot;&gt; &lt;meta content=&quot;Riseup provides online communication tools for people and groups working on liberatory social change. We are a project to create democratic alternatives and practice self-determination by controlling our own secure means of communications.&quot; name=&quot;description&quot;&gt; &lt;meta content=&quot;Home - riseup.net&quot; property=&quot;og:title&quot;&gt; &lt;meta content=&quot;website&quot; property=&quot;og:type&quot;&gt; &lt;meta content=&quot;https://riseup.net/en&quot; property=&quot;og:url&quot;&gt; &lt;meta content=&quot;https://riseup.net/about-us/images/riseup.net-inline.svg&quot; property=&quot;og:image&quot;&gt; &lt;meta content=&quot;Riseup provides online communication tools for people and groups working on liberatory social change. We are a project to create democratic alternatives and practice self-determination by controlling our own secure means of communications.&quot; property=&quot;og:description&quot;&gt; &lt;meta content=&quot;summary_large_image&quot; name=&quot;twitter:card&quot;&gt; &lt;meta content=&quot;@riseupnet&quot; name=&quot;twitter:site&quot;&gt; &lt;meta content=&quot;Home - riseup.net&quot; name=&quot;twitter:title&quot;&gt; &lt;meta content=&quot;https://riseup.net/about-us/images/card2.png&quot; name=&quot;twitter:image&quot;&gt; &lt;meta content=&quot;Riseup provides online communication tools for people and groups working on liberatory social change. We are a project to create democratic alternatives and practice self-determination by controlling our own secure means of communications.&quot; name=&quot;twitter:description&quot;&gt;  &lt;link href=&quot;/assets/bootstrap.min.css&quot; rel=&quot;stylesheet&quot;&gt; &lt;link href=&quot;/assets/font-awesome-4.6.3/css/font-awesome.min.css&quot; rel=&quot;stylesheet&quot;&gt; &lt;link href=&quot;/assets/style.css&quot; rel=&quot;stylesheet&quot;&gt; &lt;link href=&quot;/assets/images/favicon.png&quot; rel=&quot;icon&quot; type=&quot;image/x-icon&quot;&gt; &lt;base href=&quot;/en/&quot;&gt; &lt;/head&gt; &lt;body class=&quot;home&quot;&gt; &lt;div class=&quot;nav-home&quot; id=&quot;riseup-bar&quot;&gt;   &lt;div id=&quot;riseup-nav&quot;&gt;     &lt;div class=&quot;hover-item&quot;&gt;       &lt;a href=&quot;/en&quot;&gt;Riseup Home&lt;/a&gt;       &lt;div class=&quot;dropdown&quot;&gt;         &lt;div class=&quot;spacer&quot;&gt;&lt;/div&gt;         &lt;div class=&quot;menu&quot;&gt;           &lt;div class=&quot;chiclets nav-grey&quot;&gt;             &lt;a href=&quot;https://riseup.net/&quot; class=&quot;nav-home&quot;&gt;Home&lt;/a&gt;             &lt;a href=&quot;https://riseup.net/donate&quot; class=&quot;nav-donate&quot;&gt;Donate!&lt;/a&gt;           &lt;/div&gt;           &lt;div class=&quot;section nav-red&quot;&gt;Red Accounts&lt;/div&gt;           &lt;div class=&quot;chiclets nav-red&quot;&gt;             &lt;a href=&quot;https://account.riseup.net/&quot; class=&quot;nav-account&quot;&gt;Account&lt;/a&gt;             &lt;a href=&quot;https://support.riseup.net/&quot; class=&quot;nav-support&quot;&gt;Support&lt;/a&gt;             &lt;a href=&quot;https://mail.riseup.net/&quot; class=&quot;nav-email&quot;&gt;Email&lt;/a&gt;             &lt;a href=&quot;https://riseup.net/chat&quot; class=&quot;nav-chat&quot;&gt;Chat&lt;/a&gt;             &lt;a href=&quot;https://riseup.net/vpn&quot; class=&quot;nav-vpn&quot;&gt;VPN&lt;/a&gt;           &lt;/div&gt;           &lt;div class=&quot;section nav-black&quot;&gt;Black Accounts&lt;/div&gt;           &lt;div class=&quot;chiclets nav-black&quot;&gt;             &lt;a href=&quot;https://black.riseup.net/&quot; class=&quot;nav-account&quot;&gt;Account&lt;/a&gt;             &lt;a href=&quot;https://riseup.net/vpn&quot; class=&quot;nav-vpn&quot;&gt;VPN&lt;/a&gt;           &lt;/div&gt;           &lt;div class=&quot;section nav-green&quot;&gt;Other Services&lt;/div&gt;           &lt;div class=&quot;chiclets nav-green&quot;&gt;             &lt;a href=&quot;https://lists.riseup.net/&quot; class=&quot;nav-lists&quot;&gt;Lists&lt;/a&gt;             &lt;a href=&quot;https://pad.riseup.net/&quot; class=&quot;nav-pad&quot;&gt;Pad&lt;/a&gt;             &lt;a href=&quot;https://share.riseup.net/&quot; class=&quot;nav-share&quot;&gt;Share&lt;/a&gt;             &lt;a href=&quot;https://we.riseup.net/&quot; class=&quot;nav-groups&quot;&gt;Groups&lt;/a&gt;           &lt;/div&gt;         &lt;/div&gt;       &lt;/div&gt;     &lt;/div&gt;   &lt;/div&gt; &lt;/div&gt;  &lt;div id=&quot;masthead&quot;&gt; &lt;div class=&quot;container&quot;&gt;   &lt;div class=&quot;row&quot;&gt;     &lt;div class=&quot;col-sm-12&quot;&gt;       &lt;div class=&quot;masthead-inner&quot;&gt;         &lt;div class=&quot;title&quot;&gt;           &lt;div class=&quot;sitename&quot;&gt;             &lt;a href=&quot;/&quot;&gt;&lt;/a&gt;           &lt;/div&gt;         &lt;/div&gt;         &lt;ul class=&quot;list-unstyled&quot; id=&quot;top-menu&quot;&gt;           &lt;li class=&quot;first active&quot;&gt;             &lt;a class=&quot;first active&quot; href=&quot;/en&quot;&gt;Home&lt;/a&gt;           &lt;/li&gt;           &lt;li class=&quot;&quot;&gt;             &lt;a class=&quot;&quot; href=&quot;/en/email&quot;&gt;Email&lt;/a&gt;           &lt;/li&gt;           &lt;li class=&quot;&quot;&gt;             &lt;a class=&quot;&quot; href=&quot;/en/lists&quot;&gt;Lists&lt;/a&gt;           &lt;/li&gt;           &lt;li class=&quot;&quot;&gt;             &lt;a class=&quot;&quot; href=&quot;/en/vpn&quot;&gt;VPN&lt;/a&gt;           &lt;/li&gt;           &lt;li class=&quot;&quot;&gt;             &lt;a class=&quot;&quot; href=&quot;/en/security&quot;&gt;Security&lt;/a&gt;           &lt;/li&gt;           &lt;li class=&quot;&quot;&gt;             &lt;a class=&quot;&quot; href=&quot;/en/about-us&quot;&gt;About Us&lt;/a&gt;           &lt;/li&gt;         &lt;/ul&gt;       &lt;/div&gt;     &lt;/div&gt;   &lt;/div&gt; &lt;/div&gt;  &lt;/div&gt; &lt;div class=&quot;container&quot; id=&quot;main&quot;&gt; &lt;div class=&quot;row&quot;&gt; &lt;div class=&quot;col-sm-12&quot;&gt; &lt;div class=&quot;shadow-box&quot;&gt; &lt;div class=&quot;title-box&quot;&gt; &lt;div class=&quot;logo&quot;&gt; &lt;div class=&quot;summary&quot;&gt; Riseup provides online communication tools for people and groups working on liberatory social change. We are a project to create democratic alternatives and practice self-determination by controlling our own secure means of communications. &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;content-box&quot;&gt; &lt;div class=&quot;row&quot;&gt; &lt;div class=&quot;col-sm-8&quot;&gt; &lt;div class=&quot;locale-links&quot;&gt; &lt;a class=&quot;label&quot; href=&quot;/zh&quot;&gt;中文&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/es&quot;&gt;Español&lt;/a&gt; &lt;a class=&quot;label label-primary&quot; href=&quot;/en&quot;&gt;English&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/pt&quot;&gt;Português&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/ru&quot;&gt;Pyccĸий&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/de&quot;&gt;Deutsch&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/fr&quot;&gt;Français&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/it&quot;&gt;Italiano&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/pl&quot;&gt;Polski&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/el&quot;&gt;Ελληνικά&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/ca&quot;&gt;Català&lt;/a&gt; &lt;a class=&quot;label&quot; href=&quot;/hi&quot;&gt;Hindi&lt;/a&gt; &lt;/div&gt; &lt;br&gt; &lt;a href=&quot;/en/donate&quot; class=&quot;btn btn-default btn-lg&quot;&gt;Support Riseup!&lt;/a&gt;  &lt;h1 class=&quot;red&quot;&gt;   &lt;span&gt;Personal Services&lt;/span&gt; &lt;/h1&gt; &lt;p&gt;We provide accounts for traditional services, including &lt;a href=&quot;/en/email&quot;&gt;Email&lt;/a&gt; (IMAP) and &lt;a href=&quot;/en/vpn&quot;&gt;VPN&lt;/a&gt;.&lt;/p&gt; &lt;div class=&quot;row&quot;&gt;   &lt;div class=&quot;col-sm-6&quot;&gt;     &lt;ul class=&quot;fa-ul spaced&quot;&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-inbox&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://mail.riseup.net&quot;&gt;Login to webmail&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-support&quot;&gt;&lt;/i&gt;         Get help on &lt;a href=&quot;/en/email&quot;&gt;Email&lt;/a&gt; and &lt;a href=&quot;/en/vpn&quot;&gt;VPN&lt;/a&gt;.       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-toggle-on&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://account.riseup.net&quot;&gt;Change my settings&lt;/a&gt;       &lt;/li&gt;     &lt;/ul&gt;   &lt;/div&gt;   &lt;div class=&quot;col-sm-6&quot;&gt;     &lt;ul class=&quot;fa-ul spaced&quot;&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-plus-square&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://account.riseup.net/user/new&quot;&gt;Request an account&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-exclamation-circle&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://account.riseup.net/reset_password&quot;&gt;Reset lost password&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-ticket&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://support.riseup.net/en/topics/new&quot;&gt;Create a help ticket&lt;/a&gt;       &lt;/li&gt;     &lt;/ul&gt;   &lt;/div&gt; &lt;/div&gt; &lt;h1 class=&quot;black&quot;&gt;   &lt;span&gt;Mailing Lists&lt;/span&gt; &lt;/h1&gt; &lt;p&gt;We provide mailing lists for activist organizations.&lt;/p&gt; &lt;div class=&quot;row&quot;&gt;   &lt;div class=&quot;col-sm-6&quot;&gt;     &lt;ul class=&quot;fa-ul spaced&quot;&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-reply-all&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;https://lists.riseup.net/www/&quot;&gt;Login to lists&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-support&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;/en/lists&quot;&gt;Get help on lists&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-ticket&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;/en/lists/list-admin/configuration/creating-lists&quot;&gt;Request a list&lt;/a&gt;       &lt;/li&gt;     &lt;/ul&gt;   &lt;/div&gt;   &lt;div class=&quot;col-sm-6&quot;&gt;     &lt;ul class=&quot;fa-ul spaced&quot;&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-plus-square&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;/en/lists/list-user/subscribing&quot;&gt;Subscribe&lt;/a&gt;       &lt;/li&gt;       &lt;li&gt;         &lt;i class=&quot;fa-li fa fa-minus-square&quot;&gt;&lt;/i&gt;         &lt;a href=&quot;/en/lists/list-user/subscribing&quot;&gt;Unsubscribe&lt;/a&gt;       &lt;/li&gt;     &lt;/ul&gt;   &lt;/div&gt; &lt;/div&gt; &lt;h1 class=&quot;green&quot;&gt;   &lt;span&gt;Collaboration&lt;/span&gt; &lt;/h1&gt; &lt;p&gt;The following services are for group collaboration&lt;/p&gt; &lt;ul class=&quot;fa-ul spaced&quot;&gt;   &lt;li&gt;     &lt;i class=&quot;fa-li fa fa-file-text&quot;&gt;&lt;/i&gt;     &lt;b&gt;&lt;a href=&quot;https://we.riseup.net&quot;&gt;we.riseup.net&lt;/a&gt;&lt;/b&gt;     — private wikis and group collaboration.   &lt;/li&gt;   &lt;li&gt;     &lt;i class=&quot;fa-li fa fa-pencil&quot;&gt;&lt;/i&gt;     &lt;b&gt;&lt;a href=&quot;https://pad.riseup.net&quot;&gt;pad.riseup.net&lt;/a&gt;&lt;/b&gt;     — real-time collaborative text editor.   &lt;/li&gt;   &lt;li&gt;     &lt;i class=&quot;fa-li fa fa-share-alt&quot;&gt;&lt;/i&gt;     &lt;b&gt;&lt;a href=&quot;https://share.riseup.net&quot;&gt;share.riseup.net&lt;/a&gt;&lt;/b&gt;     — file upload (pastebin and imagebin).   &lt;/li&gt; &lt;/ul&gt; &lt;h3&gt;&lt;a name=&quot;resources&quot;&gt;&lt;/a&gt;Resources&lt;/h3&gt; &lt;p&gt;&lt;a href=&quot;/en/security&quot;&gt;Security&lt;/a&gt;&lt;/p&gt; &lt;p class=&quot;indent&quot;&gt;Resources and tutorials for more secure communication.&lt;/p&gt; &lt;p&gt;&lt;a href=&quot;https://support.riseup.net/en/topics/new&quot;&gt;Riseup Help Desk&lt;/a&gt;&lt;/p&gt; &lt;p class=&quot;indent&quot;&gt;In order to contact us with a question, use the help desk form to create a help ticket. But first, please search and read the online documentation found on this site.&lt;/p&gt; &lt;p&gt;&lt;a href=&quot;/en/security/resources/radical-servers&quot;&gt;Radical Servers&lt;/a&gt;&lt;/p&gt; &lt;p class=&quot;indent&quot;&gt;A directory of dozens of radical server projects around the world.&lt;/p&gt;  &lt;/div&gt; &lt;div class=&quot;col-sm-4&quot;&gt; &lt;div class=&quot;feed&quot;&gt; &lt;h2&gt;System Updates&lt;/h2&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;We need your help!&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2022-01-06&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     Riseup&apos;s services are funded by donations from people like you. We try not to ask too often, but we have to ask sometimes. Please consider making a donation if you value this freely available service, appreciate that we don&apos;t track or sell your data, or want to support people around the world working towards liberatory social change.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-warning&quot;&gt;Scheduled network outage&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2021-10-14&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     Today at 15h UTC, 1pm EDT, 10am PDT there will be a planned network outage. We anticipate it being very short, but it will likely be a few minutes long. We wanted to let you know to be aware when it will happen.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Update on switch outage&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2021-05-09&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     The switch failure has been resolved with a replacement. If you are using Thunderbird and still cannot login, please quit and restart it. Any emails that were to be delivered during the outage period are not lost, and will be delivered.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-danger&quot;&gt;Network switch outage&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2021-05-08&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     A critical failure to one of our core network switches is resulting in some people having difficulty using our services. This happened in the middle of the night, and we will need to replace the equipment, so please bear with us as we resolve this disruptive problem.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Another minor Terms of Service update!&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2021-02-19&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     We made a small change to our &lt;a href=&quot;/en/about-us/policy/tos&quot;&gt;Terms of Service&lt;/a&gt; to add this line: Do not trade, sell, publicly give away, or publicly offer invites to people you don&apos;t know.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Minor Terms of Service update&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2020-06-12&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     We made a small change to our &lt;a href=&quot;/en/about-us/policy/tos&quot;&gt;Terms of Service&lt;/a&gt; to explicitly indicate that usernames are included in the antiharassment definition.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Winter fundraising campaign&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2020-01-27&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     It&apos;s Riseup&apos;s twentieth year, help keep us going! We need your support to support each other. Please contribute to our &lt;a href=&quot;https://riseup.net/donate&quot;&gt;winter fundraising drive&lt;/a&gt;.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Happy #N30!&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2019-11-30&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     Happy N30 from your friendly autonomous tech collective, running servers for justice since 1999. Much love to all in the streets &amp;amp; behind the screens fighting for a better world. &lt;a href=&quot;/en/vpn/donate&quot;&gt;Donate to keep Riseup working hard&lt;/a&gt; for you and movements globally.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Certificate update&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2019-10-05&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     The *.riseup.net, riseup.net &lt;a href=&quot;security/network-security/certificates/riseup-signed-certificate-fingerprints.txt&quot;&gt;certificates were updated&lt;/a&gt;. If you are pinning cert fingerprints, this will be the last time these certs and signed fingerprints will be updated.   &lt;/div&gt; &lt;/div&gt; &lt;div class=&quot;item&quot;&gt;   &lt;div class=&quot;label label-success&quot;&gt;Un grand merci à SQiL for a successful translation event!&lt;/div&gt;   &lt;div class=&quot;date&quot;&gt;2019-09-26&lt;/div&gt;   &lt;div class=&quot;text&quot;&gt;     Last night several wonderful volunteers came to the &lt;a href=&quot;https://agendadulibre.qc.ca/events/2023&quot;&gt;SQiL&lt;/a&gt; event to work on translating our help pages to french. Several pages were translated, updated, and fixes made, thanks to SQiL for a second year of help! Our help pages are an excellent resource to learn more about online security, &lt;a href=&quot;https://github.com/riseupnet/riseup_help&quot;&gt;anyone can help improve them&lt;/a&gt;!   &lt;/div&gt; &lt;/div&gt;  &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;/div&gt; &lt;div id=&quot;footer&quot;&gt; &lt;div id=&quot;footer-inner&quot;&gt;   &lt;div class=&quot;container&quot;&gt;     &lt;div class=&quot;row&quot;&gt;       &lt;div class=&quot;col-sm-12&quot;&gt;         &lt;div class=&quot;footer-text&quot;&gt;           &lt;div class=&quot;text-center&quot;&gt;             This site is run by Riseup, your friendly autonomous tech collective since 1999           &lt;/div&gt;           &lt;div class=&quot;text-center&quot;&gt;             &lt;ul class=&quot;list-inline&quot;&gt;               &lt;li&gt;                 &lt;a href=&quot;/en/donate&quot;&gt;Donate!&lt;/a&gt;               &lt;/li&gt;               &lt;li&gt;                 &lt;a href=&quot;https://riseupstatus.net&quot;&gt;System Status&lt;/a&gt;               &lt;/li&gt;               &lt;li&gt;                 &lt;a href=&quot;/en/about-us&quot;&gt;About Us&lt;/a&gt;               &lt;/li&gt;               &lt;li&gt;                 &lt;a href=&quot;/en/privacy-policy&quot;&gt;Privacy Policy&lt;/a&gt;               &lt;/li&gt;             &lt;/ul&gt;           &lt;/div&gt;           &lt;div class=&quot;text-center&quot;&gt;             &lt;a href=&quot;https://github.com/riseupnet/riseup_help&quot;&gt;Please edit this site&lt;/a&gt;           &lt;/div&gt;         &lt;/div&gt;       &lt;/div&gt;     &lt;/div&gt;   &lt;/div&gt; &lt;/div&gt;  &lt;/div&gt;   &lt;/body&gt;"
m_html = unescape_entities(m_html)
p_request_model = url_model("https://bbc.com", 10,"general")
m_html_parser = static_parse_controller()
m_status, m_parsed_model = m_html_parser.on_parse_html(m_html, p_request_model)
