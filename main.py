from auto_reg_dollar_cat import DollarCat
import data.managedatabase


def run(table):
    # row = len(table/2)
    for row in table:
        data.managedatabase.show_data()
        print('user' + str(row[0]) + ": " + row[1])

        username = row[1]
        password = row[2]
        public_ip = row[5]
        ssh_username = row[6]
        ssh_password = row[7]

        if public_ip is None:
            continue

        ssh_session = data.managedatabase.connect_SSH(public_ip, ssh_username, ssh_password)

        dollar = DollarCat(username, password, ssh_session)


        try:
            user_agent = dollar.start()
            if dollar.ERROR == 3:
                data.managedatabase.update_error_code_3(public_ip)
                dollar.end_session_dollar_cat()
                print("Eror 3: cant find an element")
                continue
        except:
            continue

        try:
            dollar.download_image()
        except:
            continue

        try:
            dollar.automate_slider()
            if dollar.count == 5:
                data.managedatabase.update_error_code_3(public_ip)
                continue
        except:
            continue

        try:
            print("You are in get code")
            dollar.enter_code()
        except:
            print("Except of get code")
            continue

        try:
            code = dollar.register_status()
            if code == 1:
                dollar.end_session_dollar_cat()
                data.managedatabase.update_user_agent(user_agent, username)
                data.managedatabase.update_registered(row[1])
                print("Your account is already exist")
                continue
            elif code == 3:
                print('Network error')
                dollar.end_session_dollar_cat()
                data.managedatabase.update_error_code_3(public_ip)
                continue
        except:
            continue

        try:
            print("you are in resgister now button state")
            dollar.register_now_button()
            status = dollar.register_status()
            if status == 3:
                dollar.end_session_dollar_cat()
                data.managedatabase.update_error_code_3(public_ip)
                print('Network error')
                continue
            elif code == 1:
                dollar.end_session_dollar_cat()
                data.managedatabase.update_user_agent(user_agent, username)
                data.managedatabase.update_registered(username)
                print("Your account is already exist")
                continue
        except:
            print('error 3: register button')
            data.managedatabase.update_error_code_3(public_ip)
            continue

        dollar.end_session_dollar_cat()
        data.managedatabase.update_user_agent(user_agent, username)
        data.managedatabase.update_registered(password)
        print("Your reg is success")

    def run1(table):
        row = len(table / 2)
        for row in table:
            data.managedatabase.show_data()
            print('user' + str(row[0]) + ": " + row[1])

            username = row[1]
            password = row[2]
            public_ip = row[5]
            ssh_username = row[6]
            ssh_password = row[7]

            if public_ip is None:
                continue

            ssh_session = data.managedatabase.connect_SSH(public_ip, ssh_username, ssh_password)

            dollar = DollarCat(username, password, ssh_session)

            try:
                user_agent = dollar.start()
                if dollar.ERROR == 3:
                    data.managedatabase.update_error_code_3(public_ip)
                    dollar.end_session_dollar_cat()
                    print("Eror 3: cant find an element")
                    continue
            except:
                continue

            try:
                dollar.download_image()
            except:
                continue

            try:
                dollar.automate_slider()
                if dollar.count == 5:
                    data.managedatabase.update_error_code_3(public_ip)
                    continue
            except:
                continue

            try:
                print("You are in get code")
                dollar.enter_code()
            except:
                print("Except of get code")
                continue

            try:
                code = dollar.register_status()
                if code == 1:
                    dollar.end_session_dollar_cat()
                    data.managedatabase.update_user_agent(user_agent, username)
                    data.managedatabase.update_registered(row[1])
                    print("Your account is already exist")
                    continue
                elif code == 3:
                    print('Network error')
                    dollar.end_session_dollar_cat()
                    data.managedatabase.update_error_code_3(public_ip)
                    continue
            except:
                continue

            try:
                print("you are in resgister now button state")
                dollar.register_now_button()
                status = dollar.register_status()
                if status == 3:
                    dollar.end_session_dollar_cat()
                    data.managedatabase.update_error_code_3(public_ip)
                    print('Network error')
                    continue
                elif code == 1:
                    dollar.end_session_dollar_cat()
                    data.managedatabase.update_user_agent(user_agent, username)
                    data.managedatabase.update_registered(username)
                    print("Your account is already exist")
                    continue
            except:
                print('error 3: register button')
                data.managedatabase.update_error_code_3(public_ip)
                continue

            dollar.end_session_dollar_cat()
            data.managedatabase.update_user_agent(user_agent, username)
            data.managedatabase.update_registered(password)
            print("Your reg is success")


if __name__ == "__main__":
    try:
        table = data.managedatabase.select_data()
        run(table)
    except TimeoutError:
        table = data.managedatabase.select_data()
        run(table)
