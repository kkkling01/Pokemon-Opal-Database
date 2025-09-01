import pandas as pd

if __name__ == '__main__':
    PokeData = pd.read_csv(r"PokemonUI/resource/pokemon/pokemonData/蛋白石图鉴-图鉴.csv", converters={u'序号': str})
    # print(PokeData.head())

    for index, row in PokeData.iterrows():
        print(row['序号'])
        print(row['名称CN'])
        # print(row[2])
