use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
SELECT * FROM store WHERE is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
SELECT SUM(total) FROM sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT DISTINCT(store.store_id) FROM store INNER JOIN sale ON store.store_id = sale.store_id


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
SELECT DISTINCT(store.store_id) FROM store WHERE store.store_id NOT IN (SELECT sale.store_id FROM sale)

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT avg(total/quantity),  product.name FROM sale INNER JOIN product ON product.product_id = sale.product_id GROUP BY sale.product_id

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select product.name from sale join product on product.product_id=sale.product_id group by sale.product_id having COUNT(DISTINCT sale.store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select store.name from sale join store on store.store_id=sale.store_id group by sale.store_id having count(distinct sale.product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total = (select max(total) from sale)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale where total = (select max(total) from sale) order by date limit 1