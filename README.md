Явных тегов внутри в обоих случаях нет, логика по правилу следующего элемента

find-org
- Руководитель ФИО
- Телефоны
- Телефон(ы) по данным госзакупок
- Email
- проверка на ИНН
- проверка на КПП
- Статус
- коды ОКВЕД

входные страницы
https://www.find-org.com/okved2/49.4/page/{N}
https://www.find-org.com/okved2/49.42/page/{N}
https://www.find-org.com/okved2/49.41.1/page/{N}
https://www.find-org.com/okved2/49.41.2/page/{N}
https://www.find-org.com/okved2/49.41.3/page/{N}

открыть страницу каждой компании и забираем информацию по каждой компании

Явных тегов внутри нет, по правилу следующего элемента

Сайт K-agent
https://www.k-agent.ru/catalog/{INN}-{ORGN}

База по ИНН и ОГРН есть
Либо отдельная таблица
Либо вытащить из маппинга

По каждой странице тащить
- номер телефона
- ФИО генерального
- проверка на ИНН
- проверка на КПП
- коды ОКВЕД


Insert key for captcha
create file with 

Create 
find_org_collection_links
find_org_company_information.csv


# Usage instruction 
Copy config.pt.dist to config/config.py
extract for platform your driver and rename 
