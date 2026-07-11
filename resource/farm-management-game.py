import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from game_support import *
from model import *
from constants import *

class InfoBar(AbstractGrid):
    """InfoBar should inherit from AbstractGrid (see a3 support.py). It is a grid with 2 rows and 3
    columns, which displays information to the user about the number of days elapsed in the game,
    as well as the player's energy and money. The InfoBar should span the entire width of the farm
    and inventory combined. """
    dimensions = (2, 3)
    size = (700, 90)
    infor_title = ["Day", "Money", "Energy"]
    infor_value = [1, 0, 100]

    def __init__(self, master: Union[tk.Tk, tk.Frame], **kwargs) -> None:
        """Sets up this InfoBar to be an AbstractGrid with the appropriate number of 
        rows and columns, and the appropriate width and height (see constants.py).

         Parameters:None

         return None
        """

        super().__init__(master, self.dimensions, self.size, **kwargs)
        # use loop to give the different value to different column and row
        self.configure(bg="silver")
        # self.redraw(1,0,100)

        # info_bar = tk.Canvas(master, bg='grey', width=size[0], height=size[1])
        # info_bar.pack()

    def redraw(self, day: int, money: int, energy: int) -> None:
        """ Clears the InfoBar and redraws it to display the provided day, money, 
            and energy. E.g. in Figure 3, this method was called with day = 1, money = 0, and energy = 100.

             Parameters:
             self.info_value

            return None
        """
        self.clear()
        # store the value in the list
        self.infor_value[0] = day
        self.infor_value[1] = money
        self.infor_value[2] = energy
        # use annoutate_position to create the inforbar
        self.annotate_position((0, 0), "Day:", HEADING_FONT)
        self.annotate_position((0, 1), "Money:", HEADING_FONT)
        self.annotate_position((0, 2), "Energy:", HEADING_FONT)
        self.annotate_position((1, 0), f"{self.infor_value[0]}")
        self.annotate_position((1, 1), f"${self.infor_value[1]}")
        self.annotate_position((1, 2), f"{self.infor_value[2]}")


class FarmView(AbstractGrid):
    """FarmView should inherit from AbstractGrid (see a3 support.py). 
    The FarmView is a grid displaying the farm map, player, and plants. """

    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int], size: tuple[int, int], **kwargs) -> None:
        """ Sets up the FarmView to be an AbstractGrid 
        with the appropriate dimensions and size, and creates an instance attribute of 
        an empty dictionary to be used as an image cache.

         Parameters:
         self.image_cache


        return None
        """

        super().__init__(master, dimensions, size, **kwargs)
        self.image_cache = {}

        # self.create_text(x, y, text=self.Farm_map[int(row)][int(col)])

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], 'Plant'],
               player_position: tuple[int, int], player_direction: str) -> None:
        """Clears the farm view, then creates (on the FarmView instance) the images for the ground,
        then the plants, then the player. That is, the player and plants should render in front of the
        ground, and the player should render in front of the plants.

         Parameters:
         cell_position
         x,y
         image_size
         image_path
         imagefile
         plant_row
         plant_col
         plant_image_path
         image_file
         imagefile

         return None
        """

        self.clear()

        for row in range(len(ground)):
            for col in range(len(ground[0])):
                cell_position = (row, col)
                # get the cell mid-point
                x, y = self.get_midpoint(cell_position)
                image_size = (self.get_cell_size())
                # if the map is letter "G" then give the Grass image
                if ground[int(row)][int(col)] == "G":
                    image_path = "images/grass.png"
                    image_size = (self.get_cell_size())
                    # use get image
                    imagefile = get_image(
                        image_path, image_size, self.image_cache)

                    self.create_image(x, y, image=imagefile)
                # if the map is letter "U" then give the untilled_soil image

                if ground[int(row)][int(col)] == "U":
                    image_path = "images/untilled_soil.png"
                    # use get image
                    imagefile = get_image(
                        image_path, image_size, self.image_cache)

                    self.create_image(x, y, image=imagefile)
                # if the map is letter "S" then give the soil image
                if ground[int(row)][int(col)] == "S":
                    image_path = "images/soil.png"
                    # use get image
                    imagefile = get_image(
                        image_path, image_size, self.image_cache)
                    self.create_image(x, y, image=imagefile)
            # sef the plant on thep position
            for position, plant_name in plants.items():
                plant_row, plant_col = position
                plant_image_path = f"images/plants/{plant_name.get_name()}/stage_{plant_name.get_stage()}.png"
                plantimage = get_image(
                    plant_image_path, image_size, self.image_cache)
                self.create_image(self.get_midpoint(
                    (plant_row, plant_col)), image=plantimage)

        # set the player and the dircetion
        image_file = IMAGES.get(player_direction)
        imagefile = get_image(
            f"images/{image_file}", image_size, self.image_cache)
        self.create_image(self.get_midpoint(player_position), image=imagefile)


class ItemView(tk.Frame):
    """
    ItemView should inherit from tk.Frame. The ItemView is a frame displaying relevant information
    and buttons for a single item. There are 6 items available in the game (see the ITEMS constant in
    constants.py).
    A label containing the name of the item and the amount of the item that the player has in
    their inventory, the selling price of the item, and the buying price of the item (if the item
    can be bought; see BUY PRICES in constants.py).
    If this item can be bought, the frame should then contain a button for buying the item at
    the listed buy price.
    A button for selling the item at the listed sell price (all items can be sold).
    """

    def __init__(self, master: tk.Frame, item_name: str, amount: int, select_command:
                 Optional[Callable[[str], None]] = None, sell_command: Optional[Callable[[str],
                                                                                         None]] = None, buy_command: Optional[Callable[[str], None]] = None) -> None:
        """Sets up ItemView to operate as a tk.Frame, and creates all internal widgets. Sets the commands for the buy and sell buttons to the buy command and sell command each called with
            the appropriate item name respectively. Binds the select command to be called with the
            appropriate item name when either the ItemView frame or label is left clicked

             Parameters:
             self.name
             self.item_name
             self.Buyprice
             self.label
             self.item_name
             self.plants_amount

             return None
        """
        super().__init__(master)

        # Create internal widget
        # bind the frame that can click
        self.bind("<Button-1>", lambda event: select_command(item_name))
        self.name = item_name
        self.item_name = item_name
        self.Buyprice = BUY_PRICES.get(item_name)
        # if buyprice = None then let it equal to the 0
        if self.Buyprice == None:
            self.Buyprice = "N/A"
        self.plant_amount = amount
        # create the label to show the plant informtion like the amount and the price
        self.label = tk.Label(
            self, text=f"{self.item_name}: {self.plant_amount}\n Buy price: ${self.Buyprice}\n Sell price: ${SELL_PRICES.get(self.item_name)}")
        self.label.bind("<Button-1>", lambda event: select_command(item_name))
        # calculate the number, if the number equal to 0 that mean the frame is unselectable
        if self.plant_amount > 0:
            self.label.config(background="#fdc074")
            self.label.pack(side=tk.LEFT, fill=tk.Y)

        else:
            self.label.config(background="grey")
            self.label.pack(side=tk.LEFT, fill=tk.Y)
        # only the seed can buy
        if self.item_name == "Potato Seed" or self.item_name == "Kale Seed" or self.item_name == "Berry Seed":
            self.buy_button = tk.Button(
                self, text="Buy", command=lambda: buy_command(item_name))

            self.buy_button.pack(side=tk.LEFT)

        self.sell_button = tk.Button(
            self, text="Sell", command=lambda: sell_command(item_name))
        self.sell_button.pack(side=tk.LEFT)

    def update(self, amount: int, selected: bool = False) -> None:
        """Updates the text on the label, and the colour of this ItemView appropriately. 

            Parameters:
            amount

            return None

           """
        # judge the number and update the information
        if amount > 0 and selected == True:

            self.configure(bg="#d68f54")
            self.label.configure(
                text=f"{self.item_name}: {amount}\n Buy price: ${self.Buyprice}\n Sell price: ${SELL_PRICES.get(self.item_name)}", bg="#d68f54")
        if amount > 0 and selected == False:
            self.configure(bg="#fdc074",highlightbackground="grey",highlightthickness=1)
            self.label.configure(
                text=f"{self.item_name}: {amount}\n Buy price: ${self.Buyprice}\n Sell price: ${SELL_PRICES.get(self.item_name)}", bg="#fdc074")
        if amount == 0:
            self.configure(bg="grey",highlightbackground=INVENTORY_OUTLINE_COLOUR,highlightthickness=1)
            self.label.configure(
                text=f"{self.item_name}: {amount}\n Buy price: ${self.Buyprice}\n Sell price: ${SELL_PRICES.get(self.item_name)}", bg="grey")


class FarmGame(FarmModel):
    """FarmGame is the controller class for the overall game. The controller is responsible 
    for creating and maintaining instances of the model and view classes, event handling, 
    and facilitating communication between the model and view classes. """
    days = 1

    def __init__(self, master: tk.Tk | tk.Frame, map_file: str) -> None:
        """
        Sets up the FarmGame. This
        includes the following steps:
        - Set the title of the window.
        - Create the title banner (you must use get image).
        - Create the FarmModel instance.
        - Create the instances of your view classes, and ensure they display in the format shown
        in Figure 1.
        - Create a button to enable users to increment the day, which should have the text 'Next
        day' and be displayed below the other view classes. When this button is pressed, the
        model should advance to the next day, and then the view classes should be redrawn to
        reflect the changes in the model.
        - Bind the handle keypress method to the '<KeyPress>' event.
        - Call the redraw method to ensure the view draws according to the current model state.


         Parameters:
         self.master
         menu_bar
         self.map_file
         file_menu
         self.Farmm
         self.header
         self.label
         self.next_day
         self.info_Bar
         self.dimension
         self.farmview
         self.plants_amount
         self.Item_shop

         return None
        """
        self.master = master
        # filemenu
        menu_bar = tk.Menu(master)
        self.map_file = map_file
    # Create the file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quit", command=master.destroy)
        self.the_map_file = file_menu.add_command(
            label="Map selection", command=self.select_map)
        # Add the file menu to the menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Configure the root window with the menu bar
        master.config(menu=menu_bar)

        master.bind("<KeyPress>", self.handle_keypress)

        master.title('Farm Game')

        self.Farmm = FarmModel(self.map_file)
        # the title banner

        self.header = get_image("images/header.png", (690, 120))
        self.labal = tk.Label(self.master, image=self.header)

        self.labal.pack()
        # the next day button
        self.next_day = tk.Button(
            master, text="Next day", command=self.next_day)
        self.next_day.pack(side=tk.BOTTOM)
        # the infobar instance
        self.info_bar = InfoBar(master)
        self.info_bar.pack(side=tk.BOTTOM)
        # FarmView instance
        Farm_dimensioin = self.Farmm.get_dimensions()
        self.farmview = FarmView(master, Farm_dimensioin, (500, 500))
        self.farmview.pack(side=tk.LEFT)

        self.itemview = []
        # ItemViewinstance

        for item_name in ITEMS:
            # use loop to create 6 itemsview instance
            self.plants_amount = self.Farmm._player.get_inventory().get(item_name)
            # judge the amount to give the different color
            if self.plants_amount == None:
                self.plants_amount = 0
            if self.plants_amount != 0:
                self.Item_shop = ItemView(
                    master, item_name, self.plants_amount, self.select_item, self.sell_item, self.buy_item)
                self.Item_shop.configure(
                    bg='#fdc074', highlightbackground="grey", highlightthickness=1)
                self.Item_shop.pack(expand=tk.TRUE, fill=tk.BOTH)
            # if the amount equal to the 0
            else:
                self.Item_shop = ItemView(
                    master, item_name, self.plants_amount, self.select_item, self.sell_item, self.buy_item)
                self.Item_shop.configure(
                    bg="grey", highlightbackground=INVENTORY_OUTLINE_COLOUR, highlightthickness=1)
                self.Item_shop.pack(expand=tk.TRUE, fill=tk.BOTH)
            # add all the itemview in a list
            self.itemview.append(self.Item_shop)

        self.redraw()

    def redraw(self):
        """
        Redraws the entire game based on the current model state.

         Parameters:
         amount


         return None
        """
        # redraw the infobar
        self.info_bar.redraw(self.Farmm.get_days_elapsed(
        ), self.Farmm._player.get_money(), self.Farmm._player.get_energy())
        # redraw the farmview
        self.farmview.redraw(self.Farmm.get_map(
        ), self.Farmm.get_plants(), self.Farmm.get_player_position(), self.Farmm.get_player_direction())
        # update the itemview
        for item_name in self.itemview:

            amount = self.Farmm._player.get_inventory().get(item_name.name)
            if amount is None:
                amount = 0
            # if amount equal to None then give 0
            if self.Farmm._player.get_selected_item() == item_name.name:
                item_name.update(amount, True)
            else:
                item_name.update(amount, False)

    def handle_keypress(self, event: tk.Event) -> None:
        """
        An event handler to be called when a keypress event occurs.

         Parameters:
         key

         return None
        """
        # lower the all letter be entered from the keyboard
        key = event.keysym.lower()
        # control the player move
        if key == "w":
            self.Farmm.move_player(UP)
        if key == "a":
            self.Farmm.move_player(LEFT)
        if key == "s":
            self.Farmm.move_player(DOWN)
        if key == "d":
            self.Farmm.move_player(RIGHT)
        # control the till soil and untill soil
        if key == "t":
            self.Farmm.till_soil(self.Farmm.get_player_position())
        if key == "u":
            self.Farmm.untill_soil(self.Farmm.get_player_position())
        # plant the different plants
        if key == "p":
            if self.Farmm._player.get_selected_item() is not None and self.Farmm._player.get_inventory().get(self.Farmm._player.get_selected_item()) is not None:
                # CONVERT INTO ACTUAL POTATO TO PLANT
                if self.Farmm._player.get_selected_item() == "Potato Seed":
                    plant = PotatoPlant()
                # CONVERT INTO ACTUAL KALE TO PLANT
                if self.Farmm._player.get_selected_item() == "Kale Seed":
                    plant = KalePlant()
                # CONVERT INTO ACTUAL BERRY TO PLANT
                if self.Farmm._player.get_selected_item() == "Berry Seed":
                    plant = BerryPlant
                # ADD PLANT ON THE MAP AND REMOVE FORM STOCK
                self.Farmm.add_plant(
                    self.Farmm.get_player_position(), plant)
                self.Farmm._player.remove_item(
                    (self.Farmm._player.get_selected_item(), 1))
        # HARVEST THE PLANT
        if key == "h":
            plant = self.Farmm.harvest_plant(self.Farmm.get_player_position())
            if plant is not None:
                self.Farmm._player.add_item(plant)
        # REMOVE THE PLANT FROM THE MAP
        if key == "r":
            self.Farmm.remove_plant(self.Farmm.get_player_position())

        self.redraw()

    def select_item(self, item_name: str) -> None:
        """The callback to be given to each ItemView
            for item selection. This method should set 
            the selected item to be item name and then redraw the view

             Parameters:None

             return None
            """
        self.Farmm._player.select_item(item_name)
        self.redraw()

    def buy_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView
        for buying items. This method should cause the player to attempt to buy the item with the
        given item name, at the price specified in BUY PRICES, and then redraw the view.


         Parameters:
         self.Buyprice

         return None
        """
        self.Buyprice = BUY_PRICES.get(item_name)
        # if the Buy pice equal to Noe=ne then give 0
        if self.Buyprice == None:
            self.Buyprice = 0
        self.Farmm._player.buy(item_name, self.Buyprice)
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView
        for selling items. This method should cause the player to attempt to sell the item with the
        given item name, at the price specified in SELL PRICES, and then redraw the view.

         Parameters:
         self.sellprice

         return None
        """
        # get item price
        self.sellprice = SELL_PRICES.get(item_name)
        self.Farmm._player.sell(item_name, self.sellprice)
        self.redraw()

    def next_day(self) -> None:
        """ start a new day and reset the energy and redraw the all model

         Parameters:None

         return None
        """

        self.Farmm.new_day()
        self.redraw()

    def select_map(self) -> None:
        """
        in the fill menu can select the different map

         Parameters:
         self.map_file
         self.Farmm

         return None
        """
        map_file = filedialog.askopenfilename(title="Select Map File", filetypes=(
            ("Text Files", "*.txt"), ("All Files", "*.*")))
        # update the mapfile and  redraw the farmmodel
        if map_file:
            self.map_file = map_file
            # store new map file to self.map_file
            children = self.master.winfo_children()
            # destroy all children of root (clear the window)
            # left with just an empty window
            for child in children:
                child.destroy()
            # call play game with the empty window and the new map file
            play_game(self.master, self.map_file)


def play_game(root: tk.Tk, map_file: str) -> None:
    """1. Construct the controller instance using given map file and the root tk.Tk parameter.
        2. Ensure the root window stays opening listening for events (using mainloop).

         Parameters:None

         return None
        """
    # Implement your play_game function here
    FarmGame(root, map_file)

    # run the loop
    root.mainloop()

# the main function


def main() -> None:
    """
    1. Construct the root tk.Tk instance.
    2. Call the play game function passing in the newly created root tk.Tk instance, and the path
    to any map file you like (e.g. 'maps/map1.txt').


     Parameters:
     map_path

     return None
    """
    root = tk.Tk()
    # root.title('Farm Game')
    root.iconbitmap()
    root.geometry("700x710")
    map_path = "maps/map1.txt"

   # play game

    play_game(root, map_path)


if __name__ == '__main__':
    main()
