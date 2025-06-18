#!/bin/bash

                      ####################
                     #      Le           #
                   #        Vars       #
                  ####################

WW=$(tput setaf 7)
GREEN=$(tput setaf 2)
MAGENTA=$(tput setaf 5)
RED=$(tput setaf 1)
RZ=$(tput setaf 8)
NC=$(tput sgr0)

         ###############################################
        #    You Spin my head right round right       #
      # round when u go down when you go down down  #
     #############################################

spinner() {
local pid=$!
local spin=('⣾' '⣽' '⣻' '⢿' '⡿' '⣟' '⣯' '⣷')
local i=0
tput civis                            # wait wait WTF where did the cursor GO!!?!? >_<
while kill -0 "$pid" 2>/dev/null; do
printf "%s" "${RED}${spin[i]}${NC}"
sleep 0.1
printf "\b"
i=$(( (i+1) % 8 ))
done
tput cnorm                          # oh ok phewww there it is ^_^
printf " \b"
}

# clear clear clear clear clear clear clear clear clear clear clear clear clear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clearclear clear 
clear

# 1. Gross its  Termux uegh

printf "${RED}[+]${WW} Correct the environment Termux...${NC}"
{
pkg uninstall curl libcurl -y >/dev/null 2>&1
pkg install -y termux-exec curl libcurl python git libjpeg-turbo openssl >/dev/null 2>&1
termux-exec >/dev/null 2>&1
export LD_LIBRARY_PATH=$PREFIX/lib >/dev/null 2>&1
} & spinner
printf "\b✓\n"

# 2. Git Wars: Attack of the clones
printf "${RED}[+]${WW} Load x0_Bot...${NC}"
{
rm -rf ~/x0_Bot 2>/dev/null
git clone https://github.com/spoooky762/x0_Bot.git ~/x0_Bot >/dev/null 2>&1
} & spinner
printf "\b✓\n"

# 3. pffft whattttt Dependencies.. psshh i dont have any of them (O-O)
printf "${RED}[+]${WW} Establishing dependencies...${NC}"
{
cd ~/x0_Bot 2>/dev/null
python -m pip install --upgrade pip wheel >/dev/null 2>&1

if [ -f "requirements.txt" ]; then
pip install -r requirements.txt >/dev/null 2>&1

while read -r lib; do
[[ -z "$lib" || "$lib" == "#"* ]] && continue
clean_lib=$(echo "$lib" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1)

if ! pip show "$clean_lib" >/dev/null 2>&1; then
pip install "$lib" >/dev/null 2>&1
fi
done < requirements.txt
else
pip install requests telethon pillow python-whois pytz gradient_figlet >/dev/null 2>&1
fi
} & spinner
printf "\b✓\n"

# 4. super secret alter ego creation 
printf "${RED}[+]${WW} Setting up...${NC}"
{
if ! grep -q "alias x0_Bot=" ~/.bashrc; then
echo -e "\nalias x0_Bot='cd ~/x0_Bot && python main.py'" >> ~/.bashrc
fi
source ~/.bashrc >/dev/null 2>&1
} & spinner
printf "\b✓\n"

# is that another .. ClEaR?? 
clear

#My Code equivalent of the 20th Century Fox Movie Introduction
python3 -m gradient_figlet 'ck4sp3r' -f 'banner3-D'
echo -e "${MAGENTA}[+]{RZ}Presents${NC}"
sleep 1
python3 -m gradient_figlet 'Xero_Bot' -f 'epic'
echo -e "${RED}[+]{RZ}  Developed by cK4sp3r <3${NC}"
sleep 1
echo -e "$[RED}[+]{RZ}| github.com/spoooky762 |${NC}"
sleep 1
echo -e "${RZ}--------------------------------------------------${NC}"
echo -e "${RZ}*If the omanda does not work, run: source ~/.bashrc ${NC}"
sleep 1


                                                 # Pause for Dramatic effect..
echo -e "${MAGENTA}[+]{RZ}Starting In${NC}"
echo -e "${RED}[+]{RZ}3${NC}"
sleep 1
echo -e "${RED}[+]{RZ}2${NC}"
sleep 1
echo -e "${RED}[+]{RZ}1${NC}"
echo -e "${GREEN}[+]{RZ}Starting Now${NC}"
python3 main.py                                  # ITS ALIIVVEE











    
  






















##########################################
#    Wtf is wrong with u why r u here ?  #
#                   ...........          #
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⢀⡤⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀  .⠀⠀⠀⠀⠀    \#
#⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀.⢀      #\
#⠀⠀⡀⠀⠀⡀⠀⡔⣀⣠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠈      #\
#⠀⢠⣷⠀⢰⠇⡾⡰⣱⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      #\
#⠀⢸⢣⠀⣿⠀⣱⢁⣡⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀      #\
#⠀⢸⢸⢠⡇⠀⠋⡟⣏⠀⠀⢠⠴⠊⠉⠙⠋⠉⠉⠉⣸⠃⠀⢀⣤⢤⣐⣀⣀⠀   #\
#⠀⢸⢸⢸⡇⠀⢰⣠⡏⠀⠀⠀⠀⣠⣤⣶⡟⠳⡆⠰⠏⠀⠀⢸⣸⣟⣿⡏⢻⡛   #|
#⣄⠈⣾⡘⣧⠀⠀⣿⠀⠀⠀⠀⠚⠛⡿⡿⠧⠔⠛⠄⠀⠀⠀⡀⠀⠉⠉⠉⠉⠀    # 
#⢸⡆⠸⣧⢻⡆⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢦⡀⠀⠀⠀⠀      # 
#⢀⣧⠀⢹⡈⠁⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣀⣀⣀⡸⣦⠀⠀⠀     #  
#⠻⣿⠀⠘⢇⢠⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠋⠈⠉⠉⠀⠈⡇⠀⠀    #
#⠀⣿⣃⠀⠈⠘⡆⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣦⠇⠀⢠   #
#⠀⣿⣿⣶⣦⡴⣌⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠠⠾⠟⠛⠦⣷⠺⢋⠀⠀⠀⣸   #
#⠀⣿⢿⡅⠛⣿⡟⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠂⠀⠀⠀⠀⣠⣾⣿   #
#⠀⢻⢀⠻⡀⠘⢿⡹⣦⣄⠀⠒⠆⠀⡀⠀⠀⠀⠀⠀⠀⠀⡀⣀⣀⣠⣾⣟⣿⣿ #    
######################################             