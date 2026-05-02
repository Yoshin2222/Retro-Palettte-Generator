#Generate all the possible colours for a given system
if __name__ == "__main__":
    import math
    import os
    import time

    def generate_colours(c_format,pallete_path):
        colour_order = []
        masks = []
        bits = []
        #Split the given format into it's colour order/masks respectively
        for c in list(c_format[1]):
            try:
                int(c)
            except:
                colour_order.append(c)
            else:
                temp = (1<<int(c))-1
                masks.append(temp)
                bits.append(int(c))
#                print(bin(temp))
                1
        length = 1 << (sum(bits))
        r_masks = masks[::-1]
        print(c_format)
        colours = []
        colour_order = colour_order[::-1]#list(c_format[0])[::-1]
#        print(colour_order)
        #Define colour steps
        colour_steps = {}
        for c in range(len(colour_order)):
            colour_steps.update({colour_order[c] : math.floor(255/((1<<bits[c])-1))})
        temp_colours = {"R" : [],"G" : [],"B" : [],"A" : [],}
        #Keep a list of all possible colour values
        for colour_val in range(0,length,1):
            colours.append(colour_val)
        #From these colour values, assign RGB valus based on the mask of the colour format
        for colour in colours:
            mask = r_masks[0]# + 1 #masks[len(masks)-1]+1#]c_format[1][len(c_format[1])-1]+1
            shift = 0
            for c in range(len(colour_order)):
#                print("COLOUR =",colour,colour_order[c]," - MASK =",bin(mask))
#                print("COLOUR VAL =",(colour&mask)>>shift)
                value = ((colour&mask)>>shift) * colour_steps[colour_order[c]]
                temp_colours[colour_order[c]].append(value) #(255/(c_format[1][len(c_format[1])-1-c])+1))
                mask <<= bits[c]
                shift += bits[c]
        #Finally, go through every temp colour and generate a .act file based on the values
        act_data = []
        jasc_pal = "JASC-PAL\n0100\n{}".format(length)
        for x in range(length):
            act_data += [temp_colours["R"][x],temp_colours["G"][x],temp_colours["B"][x]]
            jasc_pal += "\n{} {} {}".format(temp_colours["R"][x],temp_colours["G"][x],temp_colours["B"][x])
        with open(os.path.join(pallete_path,"act","{}.act".format(c_format[0])),"wb") as out:
            out.write(bytes(act_data))
        with open(os.path.join(pallete_path,"pal","{}.pal".format(c_format[0])).format(c_format[0]),"w") as out:
            out.write(jasc_pal)

    def main():
        pallete_path = "system_palettes"
        formats = {
            "CPS1" : ["Capcom_CPS1","RGB444"],
            "SMS" : ["Sega_Master_System","BGR222"],
            "Genesis" : ["Sega_Genesis","BGR333"],
            "GG" : ["Sega_Game_Gear","GRB444"],
            "WSC" : ["Wonderswan_Colour","RGB444"],
            "GBA" : ["Gameboy_Advance","BGR555"],
            "SNES" : ["Super_Ninendo","BGR555"],
        }
        if not os.path.exists(pallete_path):
            os.makedirs(pallete_path)
        if not os.path.exists(os.path.join(pallete_path,"act")):
            os.makedirs(os.path.join(pallete_path,"act"))
        if not os.path.exists(os.path.join(pallete_path,"pal")):
            os.makedirs(os.path.join(pallete_path,"pal"))
        for key in formats:
            generate_colours(formats[key],pallete_path)


    main()
    print("FINISHED")
    time.sleep(1)
