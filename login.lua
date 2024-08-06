function main(splash)
    splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    splash:go("https://www.amazon.in/ap/signin")
    splash:wait(2)

    -- Fill in login form
    splash:evaljs('document.getElementById("ap_email").value = "saransh.hajare@gmail.com"')
    splash:evaljs('document.getElementById("continue").click()')
    splash:wait(2)

    splash:evaljs('document.getElementById("ap_password").value = "Saransh@amazon0605"')
    splash:evaljs('document.getElementById("signInSubmit").click()')
    splash:wait(2)

    -- Go to the reviews page
    local review_url = splash.args.url
    splash:go(review_url)
    splash:wait(2)

    return splash:html()
end
