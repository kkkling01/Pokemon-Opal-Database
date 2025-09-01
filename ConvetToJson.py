import pandas as pd

coreRise = []


def FindRisePoke(pokeRow, data):
    # riseData = pd.read_csv(r"./PokemonUI/resource/pokemon/pokemonData/蛋白石图鉴-进化.csv")
    pokeRise = []
    # print(pokeRow["进化后-"+str(0)])
    # 进化前2,进化后 3、6、9、12、15、18、21、24、27
    for i in range(9):

        if pokeRow[(i + 1) * 3] == '' or pokeRow[(i + 1) * 3] != pokeRow[(i + 1) * 3]:
            continue
        else:
            if pokeRow[(i + 1) * 3 + 1] in coreRise:
                print("进化方式已储存，跳过")
            else:
                coreRise.append(pokeRow[(i + 1) * 3 + 1])

            pokeRise.append(pokeRow[(i + 1) * 3])
            pokeRise = pokeRise + FindRisePoke(data[data['进化前'] == pokeRow[(i + 1) * 3]].values[0], data)

        # row["进化后-"+i]

    return pokeRise


if __name__ == '__main__':
    riseData = pd.read_csv(r"./PokemonUI/resource/pokemon/pokemonData/蛋白石图鉴-进化.csv")
    poke = FindRisePoke(riseData[riseData['进化前'] == '蚊香蝌蚪'].values[0], riseData)

    allpokeFi = []
    allpokeRoot = []

    for index, row in riseData.iterrows():

        if row["进化前"] in allpokeFi:
            print(row["进化前"] + "已包含，跳过")
            continue
        else:
            print(row["进化前"] + "处理中")

            allpokeFi.append(row["进化前"])
            allpokeRoot.append(row["进化前"])

            for k in FindRisePoke(row.values, riseData):
                allpokeFi.append(k)
                allpokeRoot.append(row["进化前"])

    data = {
        "叶精灵": allpokeFi,
        "根精灵": allpokeRoot,
    }
    df = pd.DataFrame(data)
    df.to_csv("PokemonRoot.csv", mode='a', index=False, header=True)

    print(coreRise)
