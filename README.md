# Потоковая обработка MOCK объявлений с маркетплейсов
Проект по "Потоковой обработке данных" СПбГУ - 2024 г.

## Задачи

* [ ] Создать генератор случайных объявлений
* [ ] Создать обработчиков данных объявлений
* [ ] Реализовать взаимодействие через Kafka

## Схема проекта

```mermaid
graph LR
	
	m1[Ozon]-->P1
	m2[Яндекс Маркет]-->P1
	m3[Wildberries]-->P1
	
	m4[Avito]-->P2
	m5[AliExpress]-->P2
	m6[...]-->P2

  m7[...]-->P3
  m8[...]-->P3

	P1(<b>Producer #1</b>) --> Kafka
	P2(<b>Producer #2</b>) --> Kafka
  P3[...] --> Kafka
	
	Kafka[<b>Kafka</b>]
	
	Kafka <--> C1(<b>Python Consumer #1</b>)
	Kafka <--> C2(<b>Python Consumer #2</b>)
	Kafka <--> C3(<b>Python Consumer #3</b>) 
```
