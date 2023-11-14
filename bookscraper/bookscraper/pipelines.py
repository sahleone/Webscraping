# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)

                value  = value[0] if type(value) is tuple else value

                adapter[field_name] = value.strip()


        ## Category and Product Type to lowercase
        lowercase_keys = ['category','product_type']

        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        # Convert Price to float
        price_keys = ['price', 'price_excl_tax','price_incl_tax','tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£','')
            adapter[price_key] = float(value)


        # Get available number of books
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0 

        else:
            availability_array = split_string_array[1].split(" ")
            adapter['availability'] = int(availability_array[0])


        # Convert number of reviews to integer
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] =  int(num_reviews_string)


        # Convert Stars to int
        mapping = {
            "zero" : 0,
            "one" : 1,
            "two" : 2,
            "three" : 3,
            "four" : 4,
            "five" : 5
        }

        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        adapter['stars'] =  mapping[stars_text_value]


        
        return item
