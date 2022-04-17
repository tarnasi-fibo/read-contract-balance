from fastapi import FastAPI
from web3 import Web3
import json
import requests
from decimal import Decimal

app = FastAPI()

accounts = [
    "0x9fdc115b263c57d13512d45f81ddbb38629bda26",
    "0x182f6ca566e42fcb789585af2a01bf9a058b5fb6",
    "0xbb91031fd30f17794b04765228ca3c5fcbb01847",
    "0x138ec722dac564195afb9fd15d7ec0015bd1483d",
    "0x7bdb5189fb664bea020ad29f39e7fa073f2d0beb",
]

bsc_rpc = "https://bsc-dataseed.binance.org/"
bsc_chain = 56
bsc_token = "BNB"
bsc_explorer = "https://bscscan.com"

fibo_bytecode = "608060408190526017805460ff60a81b1916600160a81b1790556200347a388190039081908339810160408190526200003891620005ca565b600080546001600160a01b0319163390811782556040519091907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0908290a38a516200008c90600d9060208e019062000430565b508951620000a290600e9060208d019062000430565b50600f899055620000b589600a62000715565b620000c19089620007d3565b600a819055620000d4906000196200084c565b620000e290600019620007f5565b600b55601087905560148690556011879055601285905560138590556015869055600f546200011390600a62000715565b6103e8600a546005620001279190620007d3565b620001339190620006b5565b6200013f9190620007d3565b601855600f546200015290600a62000715565b612710600a546005620001669190620007d3565b620001729190620006b5565b6200017e9190620007d3565b601955600980546001600160a01b0319166001600160a01b0385811691909117909155600b5483821660009081526003602090815260409182902092909255805163c45a015560e01b81529051879384169263c45a01559260048082019391829003018186803b158015620001f257600080fd5b505afa15801562000207573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906200022d9190620005a6565b6001600160a01b031663c9c6539630836001600160a01b031663ad5c46486040518163ffffffff1660e01b815260040160206040518083038186803b1580156200027657600080fd5b505afa1580156200028b573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190620002b19190620005a6565b6040516001600160e01b031960e085901b1681526001600160a01b03928316600482015291166024820152604401602060405180830381600087803b158015620002fa57600080fd5b505af11580156200030f573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190620003359190620005a6565b601780546001600160a01b039283166001600160a01b03199182161790915560168054848416908316179055848216600081815260066020526040808220805460ff19908116600190811790925530845282842080549091169091179055815490931690911781559051918416913480156108fc0292909190818181858888f19350505050158015620003cc573d6000803e3d6000fd5b50826001600160a01b031660006001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef600a546040516200041691815260200190565b60405180910390a3505050505050505050505050620008a5565b8280546200043e906200080f565b90600052602060002090601f016020900481019282620004625760008555620004ad565b82601f106200047d57805160ff1916838001178555620004ad565b82800160010185558215620004ad579182015b82811115620004ad57825182559160200191906001019062000490565b50620004bb929150620004bf565b5090565b5b80821115620004bb5760008155600101620004c0565b80516001600160a01b0381168114620004ee57600080fd5b919050565b600082601f83011262000504578081fd5b81516001600160401b03808211156200052157620005216200088f565b604051601f8301601f19908116603f011681019082821181831017156200054c576200054c6200088f565b8160405283815260209250868385880101111562000568578485fd5b8491505b838210156200058b57858201830151818301840152908201906200056c565b838211156200059c57848385830101525b9695505050505050565b600060208284031215620005b8578081fd5b620005c382620004d6565b9392505050565b60008060008060008060008060008060006101608c8e031215620005ec578687fd5b8b516001600160401b0381111562000602578788fd5b620006108e828f01620004f3565b60208e0151909c5090506001600160401b038111156200062e578788fd5b6200063c8e828f01620004f3565b9a505060408c0151985060608c0151975060808c0151965060a08c0151955060c08c015194506200067060e08d01620004d6565b9350620006816101008d01620004d6565b9250620006926101208d01620004d6565b9150620006a36101408d01620004d6565b90509295989b509295989b9093969950565b600082620006c757620006c762000879565b500490565b600181815b808511156200070d578160001904821115620006f157620006f162000863565b80851615620006ff57918102915b93841c9390800290620006d1565b509250929050565b6000620005c383836000826200072e57506001620007cd565b816200073d57506000620007cd565b8160018114620007565760028114620007615762000781565b6001915050620007cd565b60ff84111562000775576200077562000863565b50506001821b620007cd565b5060208310610133831016604e8410600b8410161715620007a6575081810a620007cd565b620007b28383620006cc565b8060001904821115620007c957620007c962000863565b0290505b92915050565b6000816000190483118215151615620007f057620007f062000863565b500290565b6000828210156200080a576200080a62000863565b500390565b600181811c908216806200082457607f821691505b602082108114156200084657634e487b7160e01b600052602260045260246000fd5b50919050565b6000826200085e576200085e62000879565b500690565b634e487b7160e01b600052601160045260246000fd5b634e487b7160e01b600052601260045260246000fd5b634e487b7160e01b600052604160045260246000fd5b612bc580620008b56000396000f3fe6080604052600436106102765760003560e01c80636bc87c3a1161014f578063a9059cbb116100c1578063d543dbeb1161007a578063d543dbeb14610754578063dd46706414610774578063dd62ed3e14610794578063ea2f0b37146107da578063f0f165af146107fa578063f2fde38b1461081a57600080fd5b8063a9059cbb146106a8578063aa45026b146106c8578063b2bdfa7b146106de578063b425bac3146106fe578063c49b9a801461071e578063d12a76881461073e57600080fd5b806388f820201161011357806388f82020146105e75780638da5cb5b146106205780638ee88c531461063e57806395d89b411461065e578063a457c2d714610673578063a69df4b51461069357600080fd5b80636bc87c3a1461057057806370a0823114610586578063715018a6146105a657806379af25a6146105bb5780637d1db4a5146105d157600080fd5b8063379e2919116101e8578063437823ec116101ac578063437823ec146104965780634549b039146104b657806349bd5a5e146104d65780634a74bb02146104f657806352390c02146105175780635342acb41461053757600080fd5b8063379e29191461040057806339509351146104205780633b124fe7146104405780633bd5d1731461045657806341cb87fc1461047657600080fd5b80631694505e1161023a5780631694505e1461033e57806318160ddd1461037657806323b872dd1461038b5780632d838119146103ab578063313ce567146103cb5780633685d419146103e057600080fd5b8063061c82d01461028257806306fdde03146102a4578063095ea7b3146102cf578063120a0612146102ff57806313114a9d1461031f57600080fd5b3661027d57005b600080fd5b34801561028e57600080fd5b506102a261029d3660046127dd565b61083a565b005b3480156102b057600080fd5b506102b9610872565b6040516102c6919061284d565b60405180910390f35b3480156102db57600080fd5b506102ef6102ea366004612798565b610904565b60405190151581526020016102c6565b34801561030b57600080fd5b506102a261031a3660046126e8565b61091b565b34801561032b57600080fd5b50600c545b6040519081526020016102c6565b34801561034a57600080fd5b5060165461035e906001600160a01b031681565b6040516001600160a01b0390911681526020016102c6565b34801561038257600080fd5b50600a54610330565b34801561039757600080fd5b506102ef6103a6366004612758565b610967565b3480156103b757600080fd5b506103306103c63660046127dd565b6109d0565b3480156103d757600080fd5b50600f54610330565b3480156103ec57600080fd5b506102a26103fb3660046126e8565b610a54565b34801561040c57600080fd5b506102a261041b3660046127dd565b610c43565b34801561042c57600080fd5b506102ef61043b366004612798565b610c72565b34801561044c57600080fd5b5061033060105481565b34801561046257600080fd5b506102a26104713660046127dd565b610ca8565b34801561048257600080fd5b506102a26104913660046126e8565b610d94565b3480156104a257600080fd5b506102a26104b13660046126e8565b610f66565b3480156104c257600080fd5b506103306104d13660046127f5565b610fb4565b3480156104e257600080fd5b5060175461035e906001600160a01b031681565b34801561050257600080fd5b506017546102ef90600160a81b900460ff1681565b34801561052357600080fd5b506102a26105323660046126e8565b611043565b34801561054357600080fd5b506102ef6105523660046126e8565b6001600160a01b031660009081526006602052604090205460ff1690565b34801561057c57600080fd5b5061033060145481565b34801561059257600080fd5b506103306105a13660046126e8565b611196565b3480156105b257600080fd5b506102a26111f5565b3480156105c757600080fd5b5061033060025481565b3480156105dd57600080fd5b5061033060185481565b3480156105f357600080fd5b506102ef6106023660046126e8565b6001600160a01b031660009081526007602052604090205460ff1690565b34801561062c57600080fd5b506000546001600160a01b031661035e565b34801561064a57600080fd5b506102a26106593660046127dd565b611257565b34801561066a57600080fd5b506102b9611286565b34801561067f57600080fd5b506102ef61068e366004612798565b611295565b34801561069f57600080fd5b506102a26112e4565b3480156106b457600080fd5b506102ef6106c3366004612798565b6113e0565b3480156106d457600080fd5b5061033060125481565b3480156106ea57600080fd5b5060005461035e906001600160a01b031681565b34801561070a57600080fd5b5060095461035e906001600160a01b031681565b34801561072a57600080fd5b506102a26107393660046127c3565b6113ed565b34801561074a57600080fd5b5061033060195481565b34801561076057600080fd5b506102a261076f3660046127dd565b61146f565b34801561078057600080fd5b506102a261078f3660046127dd565b6114b7565b3480156107a057600080fd5b506103306107af366004612720565b6001600160a01b03918216600090815260056020908152604080832093909416825291909152205490565b3480156107e657600080fd5b506102a26107f53660046126e8565b611526565b34801561080657600080fd5b506102a26108153660046127dd565b611571565b34801561082657600080fd5b506102a26108353660046126e8565b6115a0565b6000546001600160a01b0316331461086d5760405162461bcd60e51b8152600401610864906128a0565b60405180910390fd5b601055565b6060600d805461088190612a9e565b80601f01602080910402602001604051908101604052809291908181526020018280546108ad90612a9e565b80156108fa5780601f106108cf576101008083540402835291602001916108fa565b820191906000526020600020905b8154815290600101906020018083116108dd57829003601f168201915b5050505050905090565b6000610911338484611678565b5060015b92915050565b6000546001600160a01b031633146109455760405162461bcd60e51b8152600401610864906128a0565b600980546001600160a01b0319166001600160a01b0392909216919091179055565b600061097484848461179c565b6109c684336109c185604051806060016040528060288152602001612b23602891396001600160a01b038a1660009081526005602090815260408083203384529091529020549190611a32565b611678565b5060019392505050565b6000600b54821115610a375760405162461bcd60e51b815260206004820152602a60248201527f416d6f756e74206d757374206265206c657373207468616e20746f74616c207260448201526965666c656374696f6e7360b01b6064820152608401610864565b6000610a41611a5e565b9050610a4d8382611a81565b9392505050565b6000546001600160a01b03163314610a7e5760405162461bcd60e51b8152600401610864906128a0565b6001600160a01b03811660009081526007602052604090205460ff16610ae65760405162461bcd60e51b815260206004820152601b60248201527f4163636f756e7420697320616c726561647920696e636c7564656400000000006044820152606401610864565b60005b600854811015610c3f57816001600160a01b031660088281548110610b1e57634e487b7160e01b600052603260045260246000fd5b6000918252602090912001546001600160a01b03161415610c2d5760088054610b4990600190612a87565b81548110610b6757634e487b7160e01b600052603260045260246000fd5b600091825260209091200154600880546001600160a01b039092169183908110610ba157634e487b7160e01b600052603260045260246000fd5b600091825260208083209190910180546001600160a01b0319166001600160a01b039485161790559184168152600482526040808220829055600790925220805460ff191690556008805480610c0757634e487b7160e01b600052603160045260246000fd5b600082815260209020810160001990810180546001600160a01b03191690550190555050565b80610c3781612ad9565b915050610ae9565b5050565b6000546001600160a01b03163314610c6d5760405162461bcd60e51b8152600401610864906128a0565b601255565b3360008181526005602090815260408083206001600160a01b038716845290915281205490916109119185906109c19086611a8d565b3360008181526007602052604090205460ff1615610d1d5760405162461bcd60e51b815260206004820152602c60248201527f4578636c75646564206164647265737365732063616e6e6f742063616c6c207460448201526b3434b990333ab731ba34b7b760a11b6064820152608401610864565b6000610d2883611a99565b5050506001600160a01b038616600090815260036020526040902054939450610d5693925084915050611af4565b6001600160a01b038316600090815260036020526040902055600b54610d7c9082611af4565b600b55600c54610d8c9084611a8d565b600c55505050565b6000546001600160a01b03163314610dbe5760405162461bcd60e51b8152600401610864906128a0565b6000819050806001600160a01b031663c45a01556040518163ffffffff1660e01b815260040160206040518083038186803b158015610dfc57600080fd5b505afa158015610e10573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610e349190612704565b6001600160a01b031663c9c6539630836001600160a01b031663ad5c46486040518163ffffffff1660e01b815260040160206040518083038186803b158015610e7c57600080fd5b505afa158015610e90573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610eb49190612704565b6040516001600160e01b031960e085901b1681526001600160a01b03928316600482015291166024820152604401602060405180830381600087803b158015610efc57600080fd5b505af1158015610f10573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610f349190612704565b601780546001600160a01b039283166001600160a01b0319918216179091556016805493909216921691909117905550565b6000546001600160a01b03163314610f905760405162461bcd60e51b8152600401610864906128a0565b6001600160a01b03166000908152600660205260409020805460ff19166001179055565b6000600a548311156110085760405162461bcd60e51b815260206004820152601f60248201527f416d6f756e74206d757374206265206c657373207468616e20737570706c79006044820152606401610864565b8161102857600061101884611a99565b5094965061091595505050505050565b600061103384611a99565b5093965061091595505050505050565b6000546001600160a01b0316331461106d5760405162461bcd60e51b8152600401610864906128a0565b6001600160a01b03811660009081526007602052604090205460ff16156110d65760405162461bcd60e51b815260206004820152601b60248201527f4163636f756e7420697320616c7265616479206578636c7564656400000000006044820152606401610864565b6001600160a01b03811660009081526003602052604090205415611130576001600160a01b038116600090815260036020526040902054611116906109d0565b6001600160a01b0382166000908152600460205260409020555b6001600160a01b03166000818152600760205260408120805460ff191660019081179091556008805491820181559091527ff3f7a9fe364faab93b216da50a3214154f22a0a2b415b23a84c8169e8b636ee30180546001600160a01b0319169091179055565b6001600160a01b03811660009081526007602052604081205460ff16156111d357506001600160a01b031660009081526004602052604090205490565b6001600160a01b038216600090815260036020526040902054610915906109d0565b6000546001600160a01b0316331461121f5760405162461bcd60e51b8152600401610864906128a0565b600080546040516001600160a01b0390911690600080516020612b4b833981519152908390a3600080546001600160a01b0319169055565b6000546001600160a01b031633146112815760405162461bcd60e51b8152600401610864906128a0565b601455565b6060600e805461088190612a9e565b600061091133846109c185604051806060016040528060258152602001612b6b602591393360009081526005602090815260408083206001600160a01b038d1684529091529020549190611a32565b6001546001600160a01b0316331461134a5760405162461bcd60e51b8152602060048201526024808201527f596f7520646f6e27742068617665207065726d697373696f6e20746f20756e6c60448201526337b1b59760e11b6064820152608401610864565b60025442116113915760405162461bcd60e51b815260206004820152601360248201527221b7b73a3930b1ba1034b9903637b1b5b2b21760691b6044820152606401610864565b600154600080546040516001600160a01b039384169390911691600080516020612b4b83398151915291a3600154600080546001600160a01b0319166001600160a01b03909216919091179055565b600061091133848461179c565b6000546001600160a01b031633146114175760405162461bcd60e51b8152600401610864906128a0565b60178054821515600160a81b0260ff60a81b199091161790556040517f53726dfcaf90650aa7eb35524f4d3220f07413c8d6cb404cc8c18bf5591bc1599061146490831515815260200190565b60405180910390a150565b6000546001600160a01b031633146114995760405162461bcd60e51b8152600401610864906128a0565b600f546114a790600a6129c0565b6114b19082612a68565b60185550565b6000546001600160a01b031633146114e15760405162461bcd60e51b8152600401610864906128a0565b60008054600180546001600160a01b03199081166001600160a01b0384161790915516815560028290556040518190600080516020612b4b833981519152908290a350565b6000546001600160a01b031633146115505760405162461bcd60e51b8152600401610864906128a0565b6001600160a01b03166000908152600660205260409020805460ff19169055565b6000546001600160a01b0316331461159b5760405162461bcd60e51b8152600401610864906128a0565b601955565b6000546001600160a01b031633146115ca5760405162461bcd60e51b8152600401610864906128a0565b6001600160a01b03811661162f5760405162461bcd60e51b815260206004820152602660248201527f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160448201526564647265737360d01b6064820152608401610864565b600080546040516001600160a01b0380851693921691600080516020612b4b83398151915291a3600080546001600160a01b0319166001600160a01b0392909216919091179055565b6001600160a01b0383166116da5760405162461bcd60e51b8152602060048201526024808201527f45524332303a20617070726f76652066726f6d20746865207a65726f206164646044820152637265737360e01b6064820152608401610864565b6001600160a01b03821661173b5760405162461bcd60e51b815260206004820152602260248201527f45524332303a20617070726f766520746f20746865207a65726f206164647265604482015261737360f01b6064820152608401610864565b6001600160a01b0383811660008181526005602090815260408083209487168084529482529182902085905590518481527f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925910160405180910390a3505050565b6001600160a01b0383166118005760405162461bcd60e51b815260206004820152602560248201527f45524332303a207472616e736665722066726f6d20746865207a65726f206164604482015264647265737360d81b6064820152608401610864565b6001600160a01b0382166118625760405162461bcd60e51b815260206004820152602360248201527f45524332303a207472616e7366657220746f20746865207a65726f206164647260448201526265737360e81b6064820152608401610864565b600081116118c45760405162461bcd60e51b815260206004820152602960248201527f5472616e7366657220616d6f756e74206d7573742062652067726561746572206044820152687468616e207a65726f60b81b6064820152608401610864565b6000546001600160a01b038481169116148015906118f057506000546001600160a01b03838116911614155b15611958576018548111156119585760405162461bcd60e51b815260206004820152602860248201527f5472616e7366657220616d6f756e74206578636565647320746865206d6178546044820152673c20b6b7bab73a1760c11b6064820152608401610864565b600061196330611196565b9050601854811061197357506018545b601954811080159081906119915750601754600160a01b900460ff16155b80156119ab57506017546001600160a01b03868116911614155b80156119c05750601754600160a81b900460ff165b156119d35760195491506119d382611b00565b6001600160a01b03851660009081526006602052604090205460019060ff1680611a1557506001600160a01b03851660009081526006602052604090205460ff165b15611a1e575060005b611a2a86868684611ba7565b505050505050565b60008184841115611a565760405162461bcd60e51b8152600401610864919061284d565b505050900390565b6000806000611a6b611d47565b9092509050611a7a8282611a81565b9250505090565b6000610a4d828461295d565b6000610a4d8284612945565b6000806000806000806000806000806000611ab38c611f01565b93509350935093506000806000611ad48f878787611acf611a5e565b611f56565b919f509d509b509599509397509195509350505050919395979092949650565b6000610a4d8284612a87565b6017805460ff60a01b1916600160a01b1790556000611b20826002611a81565b90506000611b2e8383611af4565b905047611b3a83611fb8565b6000611b464783611af4565b9050611b528382612135565b60408051858152602081018390529081018490527f17bbfb9a6069321b6ded73bd96327c9e6b7212a5cd51ff219cd61370acafb5619060600160405180910390a150506017805460ff60a01b19169055505050565b80611bd157611bd16010805460115560128054601355601480546015556000928390559082905555565b6001600160a01b03841660009081526007602052604090205460ff168015611c1257506001600160a01b03831660009081526007602052604090205460ff16155b15611c2757611c22848484612219565b611d25565b6001600160a01b03841660009081526007602052604090205460ff16158015611c6857506001600160a01b03831660009081526007602052604090205460ff165b15611c7857611c2284848461235f565b6001600160a01b03841660009081526007602052604090205460ff16158015611cba57506001600160a01b03831660009081526007602052604090205460ff16155b15611cca57611c2284848461241e565b6001600160a01b03841660009081526007602052604090205460ff168015611d0a57506001600160a01b03831660009081526007602052604090205460ff165b15611d1a57611c22848484612478565b611d2584848461241e565b80611d4157611d41601154601055601354601255601554601455565b50505050565b600b54600a546000918291825b600854811015611ed157826003600060088481548110611d8457634e487b7160e01b600052603260045260246000fd5b60009182526020808320909101546001600160a01b031683528201929092526040019020541180611dfd5750816004600060088481548110611dd657634e487b7160e01b600052603260045260246000fd5b60009182526020808320909101546001600160a01b03168352820192909252604001902054115b15611e1357600b54600a54945094505050509091565b611e676003600060088481548110611e3b57634e487b7160e01b600052603260045260246000fd5b60009182526020808320909101546001600160a01b031683528201929092526040019020548490611af4565b9250611ebd6004600060088481548110611e9157634e487b7160e01b600052603260045260246000fd5b60009182526020808320909101546001600160a01b031683528201929092526040019020548390611af4565b915080611ec981612ad9565b915050611d54565b50600a54600b54611ee191611a81565b821015611ef857600b54600a549350935050509091565b90939092509050565b6000806000806000611f1286612501565b90506000611f1f87612523565b90506000611f2c8861253f565b90506000611f4682611f4085818d89611af4565b90611af4565b9993985091965094509092505050565b6000808080611f65898661255b565b90506000611f73898761255b565b90506000611f81898861255b565b90506000611f8f898961255b565b90506000611fa382611f4085818989611af4565b949d949c50929a509298505050505050505050565b6040805160028082526060820183526000926020830190803683370190505090503081600081518110611ffb57634e487b7160e01b600052603260045260246000fd5b6001600160a01b03928316602091820292909201810191909152601654604080516315ab88c960e31b81529051919093169263ad5c4648926004808301939192829003018186803b15801561204f57600080fd5b505afa158015612063573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906120879190612704565b816001815181106120a857634e487b7160e01b600052603260045260246000fd5b6001600160a01b0392831660209182029290920101526016546120ce9130911684611678565b60165460405163791ac94760e01b81526001600160a01b039091169063791ac947906121079085906000908690309042906004016128d5565b600060405180830381600087803b15801561212157600080fd5b505af1158015611a2a573d6000803e3d6000fd5b60165461214d9030906001600160a01b031684611678565b6016546001600160a01b031663f305d7198230856000806121766000546001600160a01b031690565b60405160e088901b6001600160e01b03191681526001600160a01b03958616600482015260248101949094526044840192909252606483015290911660848201524260a482015260c4016060604051808303818588803b1580156121d957600080fd5b505af11580156121ed573d6000803e3d6000fd5b50505050506040513d601f19601f820116820180604052508101906122129190612820565b5050505050565b600080600080600080600061222d88611a99565b965096509650965096509650965061227388600460008d6001600160a01b03166001600160a01b0316815260200190815260200160002054611af490919063ffffffff16565b6001600160a01b038b166000908152600460209081526040808320939093556003905220546122a29088611af4565b6001600160a01b03808c1660009081526003602052604080822093909355908b16815220546122d19087611a8d565b6001600160a01b038a166000908152600360205260409020556122f382612567565b6122fc816125f0565b61230685846126af565b886001600160a01b03168a6001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef8660405161234b91815260200190565b60405180910390a350505050505050505050565b600080600080600080600061237388611a99565b96509650965096509650965096506123b987600360008d6001600160a01b03166001600160a01b0316815260200190815260200160002054611af490919063ffffffff16565b6001600160a01b03808c16600090815260036020908152604080832094909455918c168152600490915220546123ef9085611a8d565b6001600160a01b038a166000908152600460209081526040808320939093556003905220546122d19087611a8d565b600080600080600080600061243288611a99565b96509650965096509650965096506122a287600360008d6001600160a01b03166001600160a01b0316815260200190815260200160002054611af490919063ffffffff16565b600080600080600080600061248c88611a99565b96509650965096509650965096506124d288600460008d6001600160a01b03166001600160a01b0316815260200190815260200160002054611af490919063ffffffff16565b6001600160a01b038b166000908152600460209081526040808320939093556003905220546123b99088611af4565b6000610915606461251d6010548561255b90919063ffffffff16565b90611a81565b6000610915606461251d6014548561255b90919063ffffffff16565b6000610915606461251d6012548561255b90919063ffffffff16565b6000610a4d8284612a68565b6000612571611a5e565b9050600061257f838361255b565b3060009081526003602052604090205490915061259c9082611a8d565b3060009081526003602090815260408083209390935560079052205460ff16156125eb57306000908152600460205260409020546125da9084611a8d565b306000908152600460205260409020555b505050565b60006125fa611a5e565b90506000612608838361255b565b6009546001600160a01b03166000908152600360205260409020549091506126309082611a8d565b600980546001600160a01b03908116600090815260036020908152604080832095909555925490911681526007909152205460ff16156125eb576009546001600160a01b031660009081526004602052604090205461268f9084611a8d565b6009546001600160a01b0316600090815260046020526040902055505050565b600b546126bc9083611af4565b600b55600c546126cc9082611a8d565b600c555050565b803580151581146126e357600080fd5b919050565b6000602082840312156126f9578081fd5b8135610a4d81612b0a565b600060208284031215612715578081fd5b8151610a4d81612b0a565b60008060408385031215612732578081fd5b823561273d81612b0a565b9150602083013561274d81612b0a565b809150509250929050565b60008060006060848603121561276c578081fd5b833561277781612b0a565b9250602084013561278781612b0a565b929592945050506040919091013590565b600080604083850312156127aa578182fd5b82356127b581612b0a565b946020939093013593505050565b6000602082840312156127d4578081fd5b610a4d826126d3565b6000602082840312156127ee578081fd5b5035919050565b60008060408385031215612807578182fd5b82359150612817602084016126d3565b90509250929050565b600080600060608486031215612834578283fd5b8351925060208401519150604084015190509250925092565b6000602080835283518082850152825b818110156128795785810183015185820160400152820161285d565b8181111561288a5783604083870101525b50601f01601f1916929092016040019392505050565b6020808252818101527f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572604082015260600190565b600060a082018783526020878185015260a0604085015281875180845260c0860191508289019350845b818110156129245784516001600160a01b0316835293830193918301916001016128ff565b50506001600160a01b03969096166060850152505050608001529392505050565b6000821982111561295857612958612af4565b500190565b60008261297857634e487b7160e01b81526012600452602481fd5b500490565b600181815b808511156129b857816000190482111561299e5761299e612af4565b808516156129ab57918102915b93841c9390800290612982565b509250929050565b6000610a4d83836000826129d657506001610915565b816129e357506000610915565b81600181146129f95760028114612a0357612a1f565b6001915050610915565b60ff841115612a1457612a14612af4565b50506001821b610915565b5060208310610133831016604e8410600b8410161715612a42575081810a610915565b612a4c838361297d565b8060001904821115612a6057612a60612af4565b029392505050565b6000816000190483118215151615612a8257612a82612af4565b500290565b600082821015612a9957612a99612af4565b500390565b600181811c90821680612ab257607f821691505b60208210811415612ad357634e487b7160e01b600052602260045260246000fd5b50919050565b6000600019821415612aed57612aed612af4565b5060010190565b634e487b7160e01b600052601160045260246000fd5b6001600160a01b0381168114612b1f57600080fd5b5056fe45524332303a207472616e7366657220616d6f756e74206578636565647320616c6c6f77616e63658be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e045524332303a2064656372656173656420616c6c6f77616e63652062656c6f77207a65726fa2646970667358221220bb3d28fc086233114e7afd943acdb9fcd6f7e126cb0ee6a4d935dd89b462e30b64736f6c63430008040033000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000000900000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000005ff2b0db69458a0750badebc4f9e13add608c7f000000000000000000000000000000000000000000000000000000000000dead000000000000000000000000138ec722dac564195afb9fd15d7ec0015bd1483d000000000000000000000000138ec722dac564195afb9fd15d7ec0015bd1483d00000000000000000000000000000000000000000000000000000000000000074669626f4465780000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044649424f00000000000000000000000000000000000000000000000000000000"

w3 = Web3(Web3.HTTPProvider(bsc_rpc))
f = open('fibo.json')
fibo_abi = json.load(f)


@app.get("/")
async def root():
    token_balance = {}
    contract_address = Web3.toChecksumAddress("0xF892561596B7b8085fAd1b03b902D00096AE31aD")

    contract = w3.eth.contract(address=contract_address, abi=fibo_abi)
    totalSupply = contract.functions.totalSupply().call()
    main_total = convert_to_ether(totalSupply)

    add_values = 0
    for acc in accounts:
        address = w3.toChecksumAddress(acc)
        balance = contract.functions.balanceOf(address).call()
        amount_balance = convert_to_ether(balance)
        add_values += amount_balance

    token_balance.update({"calculate": main_total - add_values})

    return token_balance['calculate']


@app.get('/total')
def total_supply():
    contract_address = Web3.toChecksumAddress("0xF892561596B7b8085fAd1b03b902D00096AE31aD")
    contract = w3.eth.contract(address=contract_address, abi=fibo_abi)
    totalSupply = contract.functions.totalSupply().call()
    main_total = convert_to_ether(totalSupply)
    return main_total


def convert_to_ether(amount):
    d_amount = Decimal(amount) * (Decimal(10) ** 14)
    return w3.fromWei(d_amount, 'ether')
