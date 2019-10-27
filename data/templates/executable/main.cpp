
#include <iostream>
#include <vector>
#include <stack>

#include <baselib/baselib.h>

#include <fiblib/CTFibonacci.h>
#include <fiblib/Fibonacci.h>


bool balanced(const std::string & braces) {
    std::string open = "({[";
    std::string close = ")}]";

    std::stack<char> stack;

    for (int i=0; i<braces.length(); i++) {
        char brace = braces[i];

        if (open.find(brace) != std::string::npos) {
            stack.push(brace);
        } else if (close.find(brace) != std::string::npos) {
            int pos = close.find(brace);
            //std::cout << pos << std::endl;

            if (stack.empty()) {
                return false;
            }

            if (stack.top() != open[pos]) {
                return false;
            }

            stack.pop();
        }
    }

    return true;
}

// Complete the braces function below.
std::vector<std::string> braces(std::vector<std::string> values) {
    std::vector<std::string> results;

    for (const std::string & value : values) {
        results.push_back(balanced(value) ? "YES" : "NO");
    }

    return results;
}


int main(int /*argc*/, char* /*argv*/[])
{
    std::cout << balanced("{[]()}") << std::endl;
    return 0;
}
