few_shots = [
    {'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "91",
     'Answer': "91"},

    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "22292",
     'Answer': "22292"},

    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied, how much revenue will our store generate?",
     'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
FROM (SELECT sum(price*stock_quantity) as total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Levi' GROUP BY t_shirt_id) a 
LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "16725.4",
     'Answer': "16725.4"},

    {'Question': "If we have to sell all the Levi’s T-shirts today, how much revenue our store will generate without discount?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
     'SQLResult': "17462",
     'Answer': "17462"},

    {'Question': "How many white color Levi's shirts do we have?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "290",
     'Answer': "290"},

    {'Question': "How much sales amount will be generated if we sell all large size t-shirts today in Nike brand after discounts?",
     'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
FROM (SELECT sum(price*stock_quantity) as total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Nike' AND size='L' GROUP BY t_shirt_id) a 
LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "290",
     'Answer': "290"},

    # NEW EXAMPLES
    {'Question': "How many Adidas t-shirts do we have in size M?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Adidas' AND size = 'M'",
     'SQLResult': "150",
     'Answer': "150"},

    {'Question': "How much inventory value do we have for all red t-shirts?",
     'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE color = 'Red'",
     'SQLResult': "45890",
     'Answer': "45890"},

    {'Question': "What is the total revenue if we sell all small size Adidas t-shirts after discount?",
     'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
FROM (SELECT sum(price*stock_quantity) as total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Adidas' AND size='S' GROUP BY t_shirt_id) a 
LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "12000",
     'Answer': "12000"},

    {'Question': "How many black color Nike t-shirts are left in stock?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'Black'",
     'SQLResult': "320",
     'Answer': "320"}
]
