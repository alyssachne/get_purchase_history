from get_purchase import get_purchase_main
import argparse

def main():
    parser = argparse.ArgumentParser(description='Get purchase information from Taobao')
    parser.add_argument('url', type=str, help='URL of the user to get purchase information from')
    args = parser.parse_args()
    
    url = args.url
    get_purchase_main(url)

if __name__ == '__main__':
    main()