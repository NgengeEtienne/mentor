## Description
This is an APIs for Admin Dashboard

#### Base URL
http://localhost:8000/

## Kitchen Management (ADMIN)

- **Create Kitchen**
  - `POST  /api/kitchen`
    ```
    {
        "kitchenImage": null,
        "kitchenName": "Kitchen B",
        "kitchenUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710926057/z4ptdtxbmb4lxlwmsern.png",
        "kitchenDescription": "Des",
        "kitchenAddress": "Add",
        "kitchenState": "Karnataka",
        "kitchenPinCode": 322145,
        "kitchenLatitude": "21.12.12",
        "kitchenLongitude": "21.21.12",
        "is_delivery_available": true,
        "kitchenCity": [
            "Bengaluru"
        ],
    }
    ```

- **Get List of Kitchens**
  - `GET  /api/kitchen`
    ```
    {
        "kitchen_id": 3,
        "kitchenImage": null,
        "kitchenName": "Kitchen B",
        "kitchenUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710926057/z4ptdtxbmb4lxlwmsern.png",
        "kitchenDescription": "Des",
        "kitchenAddress": "Add",
        "kitchenState": "Karnataka",
        "kitchenPinCode": 322145,
        "kitchenLatitude": "21.12.12",
        "kitchenLongitude": "21.21.12",
        "is_delivery_available": true,
        "kitchenCity": [
            "Bengaluru"
        ],
        "data_create_time": "2024-03-20T09:14:18.791526Z",
        "last_data_updated_time": "2024-03-20T09:14:18.791546Z"
    }
    ```

- **Retrive a specific Kitchen's Details**
  - `GET  /api/kitchen/{id}`
    ```
    {
        "kitchen_id": 3,
        "kitchenImage": null,
        "kitchenName": "Kitchen B",
        "kitchenUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710926057/z4ptdtxbmb4lxlwmsern.png",
        "kitchenDescription": "Des",
        "kitchenAddress": "Add",
        "kitchenState": "Karnataka",
        "kitchenPinCode": 322145,
        "kitchenLatitude": "21.12.12",
        "kitchenLongitude": "21.21.12",
        "is_delivery_available": true,
        "kitchenCity": [
            "Bengaluru"
        ],
        "data_create_time": "2024-03-20T09:14:18.791526Z",
        "last_data_updated_time": "2024-03-20T09:14:18.791546Z"
    }
    ```

- **Update the specific Kitchen Details**
  - `PUT  /api/kitchen/{id}`
    ```
    {
        "kitchen_id": 3,
        "kitchenImage": null,
        "kitchenName": "Kitchen B",
        "kitchenUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710926057/z4ptdtxbmb4lxlwmsern.png",
        "kitchenDescription": "Des",
        "kitchenAddress": "Add",
        "kitchenState": "Karnataka",
        "kitchenPinCode": 322145,
        "kitchenLatitude": "21.12.12",
        "kitchenLongitude": "21.21.12",
        "is_delivery_available": true,
        "kitchenCity": [
            "Bengaluru"
        ],
        "data_create_time": "2024-03-20T09:14:18.791526Z",
        "last_data_updated_time": "2024-03-20T09:14:18.791546Z"
    }
    ```

- **Deleted the specific Kitchen**
  - `DELETE  /api/kitchen/{id}`
    ```
    {
    "message": "Kitchen with id 1 deleted successfully."
    }
    ```

## Menu Management (ADMIN)
- **Create Menu**
  - `POST  /api/menu`
    ```
    {
        "dish_name": "Dish A",
        "meal_name": "",
        "menu_price": 34,
        "menu_qty": 24,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": true,
        "sunday": true,
    }
    ```

- **Get List of Menus**
  - `GET  /api/menu`
    ```
    {
        "menu_id": 1,
        "dish_name": "Dish A",
        "meal_name": "",
        "menu_price": 34,
        "menu_qty": 24,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": true,
        "sunday": true,
        "data_create_time": "2024-03-20T09:01:37.529750Z",
        "last_data_updated_time": "2024-03-20T09:01:37.529779Z"
    },
    ```

- **Retrive a specific Menu's Details**
  - `GET  /api/menu/{id}`
    ```
    {
        "menu_id": 1,
        "dish_name": "Dish A",
        "meal_name": "",
        "menu_price": 34,
        "menu_qty": 24,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": true,
        "sunday": true,
        "data_create_time": "2024-03-20T09:01:37.529750Z",
        "last_data_updated_time": "2024-03-20T09:01:37.529779Z"
    },
    ```

- **Update the specific Menu Details**
  - `PUT  /api/menu/{id}`
    ```
    {
        "dish_name": "Dish A",
        "meal_name": "",
        "menu_price": 34,
        "menu_qty": 24,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": true,
        "sunday": true,
    },
    ```

- **Deleted the specific Menu**
  - `DELETE  /api/menu/{id}`
    ```
    {
      "message": "Menu with id 1 deleted successfully."
    }


## Dish Management (ADMIN)
- **Create Dish**
  - `POST  /api/dishinfo`
    ```
    {
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2
        ],
        "meal_choices": [
            1,
            2,
            3
        ],
        "dish_name": "Dish A",
        "dish_image": null,
        "DishImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509408/rdeoldxiws7hegvrn3dw.png",
        "dish_description": "test",
        "dish_base_price": "12.00000",
        "dish_weight": "12.00000",
        "dish_availability_status": "available",
        "dish_calories": "12.00000",
        "dish_protein": "23.00000",
        "dish_carbohydrates": "32.00000",
        "dish_fat": "34.00000",
        "dish_fiber": "34.00000",
    }
    ```

- **Get List of Dishes**
  - `GET  /api/dishinfo`
    ```
    {
        "dish_id": 1,
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2
        ],
        "meal_choices": [
            1,
            2,
            3
        ],
        "dish_name": "Dish A",
        "dish_image": null,
        "DishImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509408/rdeoldxiws7hegvrn3dw.png",
        "dish_description": "test",
        "dish_base_price": "12.00000",
        "dish_weight": "12.00000",
        "dish_availability_status": "available",
        "dish_calories": "12.00000",
        "dish_protein": "23.00000",
        "dish_carbohydrates": "32.00000",
        "dish_fat": "34.00000",
        "dish_fiber": "34.00000",
        "data_create_time": "2024-03-15T13:30:10.161753Z",
        "last_data_updated_time": "2024-03-15T13:30:10.161768Z"
    }
    ```

- **Retrive a specific Dish's Details**
  - `GET  /api/dishinfo/{id}`
    ```
    {
        "dish_id": 1,
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2
        ],
        "meal_choices": [
            1,
            2,
            3
        ],
        "dish_name": "Dish A",
        "dish_image": null,
        "DishImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509408/rdeoldxiws7hegvrn3dw.png",
        "dish_description": "test",
        "dish_base_price": "12.00000",
        "dish_weight": "12.00000",
        "dish_availability_status": "available",
        "dish_calories": "12.00000",
        "dish_protein": "23.00000",
        "dish_carbohydrates": "32.00000",
        "dish_fat": "34.00000",
        "dish_fiber": "34.00000",
        "data_create_time": "2024-03-15T13:30:10.161753Z",
        "last_data_updated_time": "2024-03-15T13:30:10.161768Z"
    }
    ```

- **Update the specific Dish Details**
  - `PUT  /api/dishinfo/{id}`
    ```
    {
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2
        ],
        "meal_choices": [
            1,
            2,
            3
        ],
        "dish_name": "Dish A",
        "dish_image": null,
        "DishImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509408/rdeoldxiws7hegvrn3dw.png",
        "dish_description": "test",
        "dish_base_price": "12.00000",
        "dish_weight": "12.00000",
        "dish_availability_status": "available",
        "dish_calories": "12.00000",
        "dish_protein": "23.00000",
        "dish_carbohydrates": "32.00000",
        "dish_fat": "34.00000",
        "dish_fiber": "34.00000",
    }
    ```

- **Deleted the specific Dish**
  - `DELETE  /api/dishinfo/{id}`
    ```
    {
      "message": "Dish with id 1 deleted successfully."
    }


## Meal Management (ADMIN)
- **Create Meal**
  - `POST  /api/mealinfo`
    ```
    {
        "selected_dishes": [
            1
        ],
        "meal_name": "Meal A",
        "meal_image": null,
        "MealImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509479/hnfrldmiz6amkz8cfcng.png",
        "meal_description": "testing",
        "meal_base_price": "45.00",
        "meal_weight": "23.00",
        "meal_availability_status": "available",
        "meal_qty": [
            [
                "1",
                "54"
            ]
        ],
        "total_calories": "0.00",
        "total_protein": "0.00",
        "total_carbohydrates": "0.00",
        "total_fat": "0.00",
        "total_fiber": "0.00",
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2,
            3
        ],
        "meal_choices": [
            1,
            2,
            3
        ]
    }
    ```

- **Get List of Dishes**
  - `GET  /api/mealinfo`
    ```
    {
        "meal_id": 1,
        "selected_dishes": [
            1
        ],
        "meal_name": "Meal A",
        "meal_image": null,
        "MealImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509479/hnfrldmiz6amkz8cfcng.png",
        "meal_description": "testing",
        "meal_base_price": "45.00",
        "meal_weight": "23.00",
        "meal_availability_status": "available",
        "meal_qty": [
            [
                "1",
                "54"
            ]
        ],
        "total_calories": "0.00",
        "total_protein": "0.00",
        "total_carbohydrates": "0.00",
        "total_fat": "0.00",
        "total_fiber": "0.00",
        "data_create_time": "2024-03-15T13:31:20.080341Z",
        "last_data_updated_time": "2024-03-15T13:31:20.080360Z",
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2,
            3
        ],
        "meal_choices": [
            1,
            2,
            3
        ]
    }
    ```

- **Retrive a specific Meal's Details**
  - `GET  /api/mealinfo/{id}`
    ```
    {
        "meal_id": 1,
        "selected_dishes": [
            1
        ],
        "meal_name": "Meal A",
        "meal_image": null,
        "MealImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509479/hnfrldmiz6amkz8cfcng.png",
        "meal_description": "testing",
        "meal_base_price": "45.00",
        "meal_weight": "23.00",
        "meal_availability_status": "available",
        "meal_qty": [
            [
                "1",
                "54"
            ]
        ],
        "total_calories": "0.00",
        "total_protein": "0.00",
        "total_carbohydrates": "0.00",
        "total_fat": "0.00",
        "total_fiber": "0.00",
        "data_create_time": "2024-03-15T13:31:20.080341Z",
        "last_data_updated_time": "2024-03-15T13:31:20.080360Z",
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2,
            3
        ],
        "meal_choices": [
            1,
            2,
            3
        ]
    }
    ```

- **Update the specific Meal Details**
  - `PUT  /api/mealinfo/{id}`
    ```
    {
        "selected_dishes": [
            1
        ],
        "meal_name": "Meal A",
        "meal_image": null,
        "MealImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710509479/hnfrldmiz6amkz8cfcng.png",
        "meal_description": "testing",
        "meal_base_price": "45.00",
        "meal_weight": "23.00",
        "meal_availability_status": "available",
        "meal_qty": [
            [
                "1",
                "54"
            ]
        ],
        "total_calories": "0.00",
        "total_protein": "0.00",
        "total_carbohydrates": "0.00",
        "total_fat": "0.00",
        "total_fiber": "0.00",
        "dietary_choices": [
            2
        ],
        "cuisine_choices": [
            1,
            2,
            3
        ],
        "meal_choices": [
            1,
            2,
            3
        ]
    }
    ```

- **Deleted the specific Meal**
  - `DELETE  /api/mealinfo/{id}`
    ```
    {
      "message": "Meal with id 1 deleted successfully."
    }


## Meal-Plan Management (ADMIN)
- **Create Meal-Plan**
  - `POST  /api/mealplan`
    ```
    {
        "dietary_choices": [1],
        "cuisine_choices": [1,2,3],
        "monday_breakfast_dish": [],
        "monday_breakfast_meal": [1],
        "monday_breakfast_dish_option": [2],
        "monday_breakfast_meal_option": [],
        "monday_lunch_dish": [1],
        "monday_lunch_meal": [],
        "monday_lunch_dish_option": [],
        "monday_lunch_meal_option": [1],
        "monday_dinner_dish": [1],
        "monday_dinner_meal": [1],
        "monday_dinner_dish_option": [1],
        "monday_dinner_meal_option": [1],
        "tuesday_breakfast_dish": [1],
        "tuesday_breakfast_meal": [1],
        "tuesday_breakfast_dish_option": [],
        "tuesday_breakfast_meal_option": [1],
        "tuesday_lunch_dish": [1],
        "tuesday_lunch_meal": [],
        "tuesday_lunch_dish_option": [1],
        "tuesday_lunch_meal_option": [1],
        "tuesday_dinner_dish": [1],
        "tuesday_dinner_meal": [1],
        "tuesday_dinner_dish_option": [1],
        "tuesday_dinner_meal_option": [],
        "wednesday_breakfast_dish": [],
        "wednesday_breakfast_meal": [1],
        "wednesday_breakfast_dish_option": [1],
        "wednesday_breakfast_meal_option": [],
        "wednesday_lunch_dish": [1],
        "wednesday_lunch_meal": [],
        "wednesday_lunch_dish_option": [],
        "wednesday_lunch_meal_option": [1],
        "wednesday_dinner_dish": [],
        "wednesday_dinner_meal": [1],
        "wednesday_dinner_dish_option": [],
        "wednesday_dinner_meal_option": [1],
        "thursday_breakfast_dish": [],
        "thursday_breakfast_meal": [],
        "thursday_breakfast_dish_option": [],
        "thursday_breakfast_meal_option": [],
        "thursday_lunch_dish": [1],
        "thursday_lunch_meal": [1],
        "thursday_lunch_dish_option": [1],
        "thursday_lunch_meal_option": [1],
        "thursday_dinner_dish": [],
        "thursday_dinner_meal": [],
        "thursday_dinner_dish_option": [],
        "thursday_dinner_meal_option": [],
        "friday_breakfast_dish": [],
        "friday_breakfast_meal": [],
        "friday_breakfast_dish_option": [],
        "friday_breakfast_meal_option": [],
        "friday_lunch_dish": [],
        "friday_lunch_meal": [],
        "friday_lunch_dish_option": [],
        "friday_lunch_meal_option": [],
        "friday_dinner_dish": [1],
        "friday_dinner_meal": [1],
        "friday_dinner_dish_option": [],
        "friday_dinner_meal_option": [1],
        "saturday_breakfast_dish": [1],
        "saturday_breakfast_meal": [1],
        "saturday_breakfast_dish_option": [1],
        "saturday_breakfast_meal_option": [1],
        "saturday_lunch_dish": [],
        "saturday_lunch_meal": [],
        "saturday_lunch_dish_option": [],
        "saturday_lunch_meal_option": [],
        "saturday_dinner_dish": [],
        "saturday_dinner_meal": [],
        "saturday_dinner_dish_option": [],
        "saturday_dinner_meal_option": [],
        "sunday_breakfast_dish": [1],
        "sunday_breakfast_meal": [1],
        "sunday_breakfast_dish_option": [1],
        "sunday_breakfast_meal_option": [1],
        "sunday_lunch_dish": [1],
        "sunday_lunch_meal": [1],
        "sunday_lunch_dish_option": [1],
        "sunday_lunch_meal_option": [1],
        "sunday_dinner_dish": [],
        "sunday_dinner_meal": [1],
        "sunday_dinner_dish_option": [1],
        "sunday_dinner_meal_option": [],
        "meal_plan_name": "Meal - Plan Final Test",
        "meal_plan_image": null,
        "MealPlanImgUrl": "http://res.cloudinary.com/djmhrkv5t/image/upload/v1710774160/qxhlop5jf6ub79pzrx6j.png",
        "meal_plan_description": "test",
        "meal_plan_availability_status": "available",
        "daily_price": "34.00",
        "daily_breakfast_price": "29.00",
        "daily_lunch_price": "21.00",
        "daily_dinner_price": "45.00",
        "weekly_price": "767.00",
        "weekly_breakfast_price": "453.00",
        "weekly_lunch_price": "675.00",
        "weekly_dinner_price": "322.00",
        "monthly_price": "3432.00",
        "monthly_breakfast_price": "4322.00",
        "monthly_lunch_price": "6565.00",
        "monthly_dinner_price": "7676.00",
        "is_monday_available": true,
        "is_tuesday_available": true,
        "is_wednesday_available": true,
        "is_thursday_available": true,
        "is_friday_available": true,
        "is_saturday_available": true,
        "is_sunday_available": true,
    }
    ```

- **Get List of Dishes**
  - `GET  /api/mealplan`
    ```
    {
      //same as post (additional-id and creation date get)
    }
    ```

- **Retrive a specific Meal's Details**
  - `GET  /api/mealplan/{id}`
    ```
    {
      //same as post (additional-id and creation date get)
    }
    ```

- **Update the specific Meal Details**
  - `PUT  /api/mealplan/{id}`
    ```
    {
      //same as post (additional-id and creation date get)
    }
    ```

- **Deleted the specific Meal**
  - `DELETE  /api/mealplan/{id}`
    ```
    {
      "message": "Meal-plan with id 1 deleted successfully."
    }

## Order Management (ADMIN)

- **Get List of Orders**
  - `GET  /api/user_orders`
    ```
    {
    
    }
    ```

- **Retrive a specific User Order's Details**
  - `GET  /api/user_orders/{id}`
    ```
    {
    
    }
    ```

- **Update the specific User Order Details**
  - `PUT  /api/user_orders/{id}`
    ```
    {
    
    }
    ```

- **Deleted the specific User Order**
  - `DELETE  /api/user_orders/{id}`
    ```
    {
    
    }
    
