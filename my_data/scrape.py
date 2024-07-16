import bs4 as bs
import requests as req
import pandas as pd

# big list of brands we wanna look for in the car titles
brands = ['GMC', 'Honda', 'Nissan', 'Dodge', 'Toyota', 'Ford', 'Volkswagen', 'Chevrolet', 'Dodge', 'Mazda', 'BMW', 'Kia', 'Hyundai', 'Audi']

def get_data(url: str):
    print('Scraping data...')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = req.get(url, headers=headers)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        print("Failed to retrieve the page")
        return
    else:
        print("Page retrieved successfully")

    cars = soup.find_all('article', class_='srp-list-item')
    if cars is None:
        print("No cars found")
        return
    data = []

    for car in cars:
        title = car.find('h3', class_='srp-list-item-basic-info-model').text
        make = 'N/A'
        for brand in brands:
            if brand in title:
                make = brand
            else:
                continue
        price_div = car.find('div', class_='srp-list-item__price srp-list-item__section')
        price = price_div.text.strip() if price_div else 'N/A'

        info = car.find_all('span', class_='srp-list-item__basic-info-value')
        body_style = next((info_item.text for info_item in info if "Body Style:" in info_item.text), 'N/A').replace('Body Style: ', '')
        mileage = next((info_item.text for info_item in info if "Mileage:" in info_item.text), 'N/A').replace('Mileage: ', '')
        mpg = next((info_item.text for info_item in info if "MPG:" in info_item.text), 'N/A').replace('MPG: ', '')
        mpg2: int = 0
        charcount = 1
        if mpg != 'N/A':
            # it appears that the two values for MPG are about 12 mpg apart, so we can add the middle value to 
            # approximate the mpg on average.
            mpg2=int(mpg[:2])+6
        else:
            continue
            
                
        services_span = car.find('span', class_='count')
        services = services_span['data-count'] if services_span else 'N/A'

        data.append([make, price, body_style, mileage, mpg2, services])

    df = pd.DataFrame(data, columns=['Make', 'Price', 'Body Style', 'Mileage', 'MPG', 'Services'])
    df.to_csv('car_data.csv', index=False)
    print('Data saved to car_data.csv')

get_data('https://www.carfax.com/Used-Sedans_bt7')