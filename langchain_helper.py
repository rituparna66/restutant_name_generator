from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key = "openai-api_key"
)

name_prompt = PromptTemplate(
    input_variables=["cuisine"],
    template=(
        "I want to open a restaurant for {cuisine} cuisine.\n"
        "Suggest ONE fancy, unique restaurant name.\n"
        "Reply with ONLY the name and nothing else."
    ),
)

menu_prompt = PromptTemplate(
    input_variables=["restaurant_name"],
    template=(
        "Suggest SOME menu items for a restaurant called \"{restaurant_name}\".\n"
        "Return ONLY the items as a comma separated list."
    ),
)

name_chain = name_prompt | llm
menu_chain = menu_prompt | llm


def generate_restaurant_name_and_items(cuisine: str) -> dict:
    # ---- STEP 1: Restaurant name ----
    name_msg = name_chain.invoke({"cuisine": cuisine})
    raw_name = getattr(name_msg, "content", str(name_msg)).strip()
    restaurant_name = raw_name.split("\n")[0].split(",")[0].strip()

    # ---- STEP 2: Menu items ----
    menu_msg = menu_chain.invoke({"restaurant_name": restaurant_name})
    raw_menu = getattr(menu_msg, "content", str(menu_msg)).strip()

    cleaned = raw_menu.replace("\n", ",")
    items = [
        it.strip(" .•\t-")
        for it in cleaned.split(",")
        if it.strip()
    ]

    return {
        "restaurant_name": restaurant_name,
        "menu_items": items,
    }



if __name__ == "__main__":
    result = generate_restaurant_name_and_items("Italian")
    print("Restaurant name:", result["restaurant_name"])
    print("Menu items:")
    for item in result["menu_items"]:
        print("-", item)
