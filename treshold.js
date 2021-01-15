var windowedFrames = []; //2D array - [][]

windowedFrames = [ //Simulated data
    [5, 2, 4, 7, 2, 2], //sum(x^2) = 102
    [8, 5, 4, 7, 8, 4],
    [6, 4, 8, 5, 1, 5],
    [9, 5, 3, 4, 4, 1],
    [6, 4, 2, 4, 4, 1],
]

//__________Initialization output data__________
const out = {
    tresholdEnergy: 0,
    size: 0,
    sum: 0,
    booleanFrameEnergy: 0
}

//__________While loop__________
var whileData = []; //Converted frames to 1D array of their energy
for (let i = 0; i < windowedFrames.length; i++) //windowedFrames = [i][j]
{
    whileData.push(0);
    for (let j = 0; j < windowedFrames[i].length; j++)
        whileData[i] = Math.pow(windowedFrames[i][j], 2) + whileData[i];
}

//__________Sorting array by ASC__________
whileData.sort((b, a) => { return b - a });
//__________Splitting 1D array to two 1D__________
const idx = 14;
var maxIdx = idx;
if (idx > whileData.length) //Limit of size
    var maxIdx = whileData.length;
var firstArray = [];
for (let i = 0; i < maxIdx; i++)
    firstArray.push(whileData[i]);
//__________Estimate mean of firstArray__________
var mean = (firstArray.reduce((a, b) => a + b, 0) / firstArray.length);
//__________Boolean frame energy__________
out.tresholdEnergy = mean * 10;
for (let i = 0; i < whileData.length; i++)
    if (whileData[i] > out.tresholdEnergy)
        out.booleanFrameEnergy = 1; 
        //This is true but there was required convert to int

//__________Finish rest of calculations__________
out.size = whileData.length;
out.sum = whileData.reduce((a,b) => a + b, 0); //sum of all array's elements


console.log(out);