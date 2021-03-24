import preprocess
import summarizer

def run():
    data = preprocess.pre_run()
    summarizer.summarize(data)

if __name__ == '__main__':
    print("Processing...")
    run()
    print("Finshed...")