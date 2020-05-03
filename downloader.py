from cdqa.utils.download import download_model

if __name__ == '__main__':
    print("Downloading...")
	download_model(model='distilbert-squad_1.1', dir='./models')
