from SeltosBuilder import SeltosBuilder
from CarAgent import CarAgent

def main():
    seltos_builder = SeltosBuilder()
    agent = CarAgent(seltos_builder)
    agent.build_car()
    car = agent.get_car()
    print(car)

if __name__ == '__main__':
    main()