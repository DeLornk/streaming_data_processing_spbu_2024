# Потоковая обработка MOCK объявлений с маркетплейсов
Проект по "Потоковой обработке данных" СПбГУ - 2024 г.

## Общая схема проекта

```mermaid
graph LR
	
	m1[Ozon]-->P1
	m2[Яндекс Маркет]-->P1
	m3[Wildberries]-->P1
	


	P1(<b>Producer #1</b>) --> Kafka

	
	Kafka[<b>Kafka</b>]
	
	Kafka <--> Click(<b>ClickHouse</b>)
	
	Click-->Streamlit(<b>Streamlit</b>)
	
	
	style Streamlit fill:#FF4B4B,stroke:#333,stroke-width:4px,color:#fff
    style Click fill:#F7C600,stroke:#333,stroke-width:4px
    style Kafka fill:#A9F0D1,stroke:#333,stroke-width:4px
    style P1 fill:#FFF7F8,stroke:#333,stroke-width:3px
    style m1 fill:#FFF7F8,stroke:#333,stroke-width:1px
    style m2 fill:#FFF7F8,stroke:#333,stroke-width:1px
    style m3 fill:#FFF7F8,stroke:#333,stroke-width:1px
```

## Запуск

1. Запускаем docker compose up
	```bash
	docker compose up
	```
2. Создаём producer:
	```bash
	python producer.py worker
	```
3. Далее запускаем Streamlit
	```bash
	streamlit run streamlit.py
	```
 
