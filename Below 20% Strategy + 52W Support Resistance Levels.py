//@version=5
indicator("Below 20% Strategy + 52W Support/Resistance Levels @FREEZRX", overlay = true)

// Inputs
posColorInput = input.color(color.new(#089981, 90), "Positive Color")
negColorInput = input.color(color.new(#f23645, 90), "Negative Color")
supportResistanceColor = input.color(color.new(color.blue, 0), "52W Support/Resistance Color")
transparencyInput = input.int(50, title="Transparency for -20% Level", minval=0, maxval=100)

// Calculating 52-Week High and Low
high52W = ta.highest(high, 52 * 5)  // 52 weeks * 5 trading days per week
low52W = ta.lowest(low, 52 * 5)

// Utility Functions
changePercentString(value, base) =>
    round = (value / base) * 100 - 100
    (round >= 0 ? "+" : "") + str.tostring(round, format.percent)

deletePastDrawings() =>
    for _label in label.all
        _label.delete()
    for _line in line.all
        _line.delete()

calcColor(price, comparedTo, transp = 0) => 
    color.new(price >= comparedTo ? posColorInput : negColorInput, transp)

// Drawing Function for Targets
drawTarget(price, labelText, currLine, basePrice, YearFromNow, transp=0, lineColor=color.blue) =>
    priceChange = changePercentString(price, basePrice)
    label.new(YearFromNow, price, labelText + " " + priceChange, color = calcColor(price, basePrice, transp), textcolor = color.white, xloc = xloc.bar_time, style = label.style_label_right)
    l = line.new(time, basePrice, YearFromNow, price, color = lineColor, xloc = xloc.bar_time, style = line.style_dotted)
    linefill.new(currLine, l, price > basePrice ? posColorInput : negColorInput)

// Variables globales pour la gestion de l'affichage
var float buyPrice20 = na
var targetShown = false
var float currentPrice = na 

// Get the current price and update dynamically on every bar
currentPrice := close

// Calculate dynamic Buy Price (-20%) level based on current price
buyPrice20 := currentPrice * 0.80

// Draw the support and resistance levels on the 52-week range
if not na(currentPrice)
    // Supprimer les dessins précédents
    deletePastDrawings()
    
    YearFromNow = time + timeframe.in_seconds("12M") * 1000
    currLine = line.new(time, currentPrice, YearFromNow, currentPrice, xloc.bar_time, color = color.blue, style = line.style_dotted)
    
    // Draw Buy Price -20% level
    drawTarget(buyPrice20, "BP -20%", currLine, currentPrice, YearFromNow, transparencyInput)
    
    // Draw 52W High and Low levels
    drawTarget(high52W, "52W High", currLine, currentPrice, YearFromNow, 0, supportResistanceColor)
    drawTarget(low52W, "52W Low", currLine, currentPrice, YearFromNow, 0, supportResistanceColor)
    
    targetShown := true

// If no target is displayed, show a warning table
if barstate.islast and not targetShown 
    t = table.new(position.top_right, 1, 1, chart.fg_color)
    warningText = "No analyst predictions found."
    if barstate.isconfirmed    
        warningText += "\nIf there are any new predictions for this symbol, they should appear once the market opens."
    t.cell(0, 0, warningText, text_color = chart.bg_color)

// Plot the 52W support and resistance levels on the price scale
plot(high52W, "52W High", color = supportResistanceColor, display = display.price_scale, linewidth=2)
plot(low52W,  "52W Low",  color = supportResistanceColor, display = display.price_scale, linewidth=2)

// Plot the dynamically calculated Buy Price -20% level on the price scale
plot(buyPrice20, title="BP -20%", color = calcColor(buyPrice20, currentPrice, transparencyInput), display = display.price_scale, linewidth=2)

//@FREEZRX

