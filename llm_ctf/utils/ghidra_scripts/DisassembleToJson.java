import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.HashMap;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import ghidra.app.script.GhidraScript;
import ghidra.app.util.EolComments;
import ghidra.program.model.listing.CodeUnit;
import ghidra.program.model.listing.CodeUnitFormat;
import ghidra.program.model.listing.CodeUnitFormatOptions;
import ghidra.program.model.listing.CodeUnitIterator;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.listing.Variable;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.symbol.Symbol;
import ghidra.app.util.template.TemplateSimplifier;
import ghidra.app.util.viewer.field.EolExtraCommentsOption;

import com.google.gson.*;

public class DisassembleToJson extends GhidraScript {
    private static Logger log;

    public DisassembleToJson() {
        log = LogManager.getLogger(DisassembleToJson.class);
    }

	private String getBytes(CodeUnit cu) {
        StringBuffer bytesbuf = new StringBuffer();
		try {
			byte[] bytes;
			if (cu instanceof Instruction instr) {
				bytes = instr.getParsedBytes();
			}
			else {
				bytes = cu.getBytes();
			}
			for (int i = 0; i < bytes.length; ++i) {
				if (bytes[i] >= 0x00 && bytes[i] <= 0x0F) {
					bytesbuf.append("0");
				}
				bytesbuf.append(Integer.toHexString(bytes[i] & 0xff));
			}
		}
        catch (MemoryAccessException e) {
            return "";
        }
        return bytesbuf.toString();
	}

	private String getOperands(CodeUnit cu, CodeUnitFormat cuFormat) {
        StringBuffer buffy = new StringBuffer();
		if (cu instanceof Instruction) {

			Instruction inst = (Instruction) cu;

			int opCnt = inst.getNumOperands();
			String firstSeparator = ((Instruction) cu).getSeparator(0);

			String[] opSeparators = new String[opCnt];
			String[] opReps = new String[opCnt];
			for (int i = 0; i < opCnt; ++i) {
				opReps[i] = cuFormat.getOperandRepresentationString(cu, i);
				opSeparators[i] = ((Instruction) cu).getSeparator(i + 1);
				if (opSeparators[i] == null) {
					opSeparators[i] = "";
				}
			}

			if (firstSeparator != null) {
				buffy.append(firstSeparator);
			}
			for (int i = 0; i < opCnt; ++i) {
                buffy.append(opReps[i]);
				buffy.append(opSeparators[i]);
			}
		}
		else if (cu instanceof Data) {
			Data data = (Data) cu;
			String opRep = cuFormat.getDataValueRepresentationString(data);
			buffy.append(opRep);
		}
        return buffy.toString();
	}

    private String getVariableSorageString(Variable var) {
        String offsetStr;
        if (var.isStackVariable()) {
            int offset = var.getStackOffset();
            offsetStr =
                (offset >= 0 ? " 0x" + Integer.toHexString(offset) : "-0x" + Integer.toHexString(-offset));
        }
        else if (var.isRegisterVariable()) {
            offsetStr = var.getRegister().getName();
        }
        else {
            offsetStr = var.getVariableStorage().toString();
        }
        return offsetStr;
    }

    public void export(String filename) {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        File outputFile = new File(filename);
        HashMap<String, String> json_dict = new HashMap<String, String>();

        // Formatter for disassembled code
        TemplateSimplifier simplifier = new TemplateSimplifier();
		simplifier.setEnabled(false);
        CodeUnitFormatOptions formatOptions = new CodeUnitFormatOptions(
            CodeUnitFormatOptions.ShowBlockName.NEVER,
            CodeUnitFormatOptions.ShowNamespace.NON_LOCAL,
            null,
            true, // doRegVariableMarkup
            true, // doStackVariableMarkup
            true, // includeInferredVariableMarkup
            true, // alwaysShowPrimaryReference
            true, // includeScalarReferenceAdjustment
            true, // showLibraryInNamespace
            true, // followReferencedPointers
            simplifier
        );
        var cuf = new CodeUnitFormat(formatOptions);

        // Annoying thing: for some reason catch blocks are not considered part of
        // a function (listing.getFunctionContaining() returns null), so we'll just
        // keep track of the last function we saw and assume that the next code unit
        // belongs to the same function if it's not in a function.

        ghidra.program.model.listing.Function lastFunc = null;
        CodeUnitIterator cuIterator = currentProgram.getListing().getCodeUnits(true);
        Listing listing = currentProgram.getListing();
        for (var cu : cuIterator) {
            var currentAddress = cu.getMinAddress();
			var func = listing.getFunctionContaining(currentAddress);
            if (func == null) {
                if (cu instanceof Instruction && lastFunc != null) {
                    log.warn(String.format(
                        "Instruction at [%s] not in a function; assuming it's part of %s",
                        currentAddress, lastFunc
                    ));
                    func = lastFunc;
                }
                else {
                    // System.err.printf(
                    //     "[%s] Note: skipping CU of type %s\n",
                    //     currentAddress, cu.getClass().getName()
                    // );
                    continue;
                }
            }
            lastFunc = func;
			boolean isFunctionEntryPoint = func.getEntryPoint().equals(currentAddress);
            // Get the code for this function so far, or create a new one
            String code = json_dict.getOrDefault(func.getName(), "");

            // If this is the first code unit in the function, add preamble
            if (isFunctionEntryPoint) {

                log.info(String.format(
                    "Processing: %s [%s,%s]",
                    func.getName(),
                    func.getBody().getMinAddress(),
                    func.getBody().getMaxAddress()
                ));
                // Add comment with function signature
                code += String.format("; %s\n", func.getPrototypeString(true, true));
                // Add comment with parameters
                code += "; Parameters:\n";
                for (var v : func.getParameters()) {
                    code += String.format("; %-14s %-14s %s\n",
                        v.getName(), v.getDataType().getDisplayName(), getVariableSorageString(v)
                    );
                }
                // Add comment with local variables on the stack
                code += "; Stack variables:\n";
                for (var v : func.getLocalVariables()) {
                    code += String.format("; %-14s %-14s %s\n",
                        v.getName(), v.getDataType().getDisplayName(), getVariableSorageString(v)
                    );
                }
            }
            String addrString = cu.getAddressString​(true, false);
            // Any pre-comment
            String preComment = cu.getComment(CodeUnit.PRE_COMMENT);
            if (preComment != null) {
                code += String.format("%-16s %-16s ; %s\n",
                    "",
                    "",
                    preComment
                );
            }

            // Primary symbol name (either function name or label)
            Symbol primarySymbol = cu.getPrimarySymbol();
            if (primarySymbol != null) {
                code += String.format("%-16s %-16s %s:\n", "", "", primarySymbol.getName());
            }

            // Disassembly
            code += String.format("%-16s %-16s     %-11s %-40s",
                addrString,
                getBytes(cu),
                cu.getMnemonicString(),
                getOperands(cu, cuf),
                cuf.getRepresentationString(cu, true)
            );

            // EOL comments
            EolExtraCommentsOption eolOption = new EolExtraCommentsOption();
            EolComments eolComments = new EolComments(cu, true, 6 /* arbitrary */, eolOption);
            List<String> comments = eolComments.getComments();
            if (comments.size() > 0) {
                code += "     ; " + String.join(", ", comments);
            }

            // Trim trailing whitespace
            code = code.stripTrailing();
            code += "\n";

            // Any post-comment
            String postComment = cu.getComment(CodeUnit.POST_COMMENT);
            if (postComment != null) {
                code += String.format("%-16s %-16s ; %s\n",
                    "",
                    "",
                    postComment
                );
            }

            // Update the code for this function
            json_dict.put(func.getName(), code);
        }

        // Convert the HashMap to JSON
        String json = gson.toJson(json_dict);

        // Write JSON to file
        try (FileWriter writer = new FileWriter(outputFile)) {
            writer.write(json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        export(args[0]);
    }
}
